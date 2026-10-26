"""Outcome-free analyses: O1 artefact burden, O2 spurious fraction, O3 exposure
misclassification, O6 episode probabilities and rule, V3 physiological checks, C3 NIBP cuff.
Writes out/descriptive/*.csv and summary.json."""
import hashlib
import json
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models import ROOT, CACHE
from analysis import descriptive_cohort, raw, WIDE
from pipelines import FILTERS

OUT = os.path.join(ROOT, 'out', 'descriptive')
B = 1000
rng = np.random.default_rng(7)


def cluster_ci(df, num, den, by='caseid', B=B):
    """Ratio of sums with case-cluster bootstrap CI (one case per patient)."""
    g = df.groupby(by)[[num, den]].sum()
    est = g[num].sum() / g[den].sum()
    idx = rng.integers(0, len(g), (B, len(g)))
    n, d = g[num].to_numpy()[idx].sum(1), g[den].to_numpy()[idx].sum(1)
    lo, hi = np.percentile(n / d, [2.5, 97.5])
    return est, lo, hi


def wilson(k, n, z=1.96):
    if n == 0:
        return np.nan, np.nan, np.nan
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return p, c - h, c + h


def main():
    os.makedirs(OUT, exist_ok=True)
    c = descriptive_cohort()
    S = dict(n_cases=len(c))
    desc = c
    # ---- table 1 (descriptive cohort)
    t1 = dict(age=c.age.describe().to_dict(), female=float((c.sex == 'F').mean()),
              asa3=float((c.asa >= 3).mean()), emop=float(c.emop.mean()),
              dept=c.department.value_counts().to_dict(), approach=c.approach.value_counts().to_dict(),
              ane_dur_h=c.ane_dur_h.describe().to_dict(), period_min=c.period_min.describe().to_dict(),
              transplant=int((c.optype == 'Transplantation').sum()))
    S['table1'] = t1

    # ---- O1 artefact burden
    fr = [k for k in c.columns if k.startswith('frac_')]
    w = c.period_min
    S['o1_time_fraction'] = {k[5:]: float((c[k] * w).sum() / w.sum()) for k in fr}
    hrs = w.sum() / 60
    S['o1_runs_per_hour'] = {k[5:]: float(c[k].sum() / hrs) for k in c.columns if k.startswith('runs_')}
    S['o1_total_hours'] = float(hrs)
    S['o1_cases_with_any'] = {k[5:]: float((c[k] > 0).mean()) for k in c.columns if k.startswith('runs_')}

    # ---- O2 spurious fraction by filter x resolution (T = 65)
    o2 = pd.read_pickle(os.path.join(CACHE, 'o2.pkl'))
    o2 = o2[o2.caseid.isin(c.index)]
    rows = []
    for (res, f), g in o2.groupby(['res', 'filter']):
        e, lo, hi = cluster_ci(g, 'spurious', 'low')
        ei, loi, hii = cluster_ci(g, 'indeterminate', 'low')
        rows.append(dict(res=res, filter=f, low_min=g.low.sum(), spurious_min=g.spurious.sum(),
                         spurious_frac=e, lo=lo, hi=hi, confirmed_frac=g.confirmed.sum() / g.low.sum(),
                         bridged_low_frac=g.bridged_low.sum() / g.low.sum(),
                         indeterminate_frac=ei, ind_lo=loi, ind_hi=hii,
                         masked_min=g.masked.sum(), masked_per_low=g.masked.sum() / g.low.sum(),
                         spur_g1=g.spur_g1.sum(), spur_g2=g.spur_g2.sum(), spur_g3=g.spur_g3.sum(),
                         spur_g0=g.spur_g0.sum(),
                         patients_with_spurious=int((g.spurious > 0).sum())))
    o2t = pd.DataFrame(rows)
    o2t.to_csv(os.path.join(OUT, 'o2_spurious.csv'), index=False)

    # ---- O3 exposure misclassification vs reference (binary >= 10 min < 65; minutes)
    rows = []
    bands = [(0, 5), (5, 10), (10, 15), (15, 20), (20, 1e9)]
    for f in FILTERS:
        for r in ['R1', 'R2', 'R3', 'R4', 'R5']:
            ref = raw('ref', 'bridged', r, 0, 65, 'minutes').reindex(c.index).to_numpy()
            pip = raw('pipe', f, r, 0, 65, 'minutes').reindex(c.index).to_numpy()
            rb, pb = ref >= 10, pip >= 10
            tp, tn = (rb & pb).sum(), (~rb & ~pb).sum()
            fp, fn = (~rb & pb).sum(), (rb & ~pb).sum()
            n = len(rb)
            po = (tp + tn) / n
            pe = ((tp + fp) * (tp + fn) + (tn + fn) * (tn + fp)) / n ** 2
            diff = pip - ref
            row = dict(filter=f, res=r, prev_ref=rb.mean(), prev_pipe=pb.mean(),
                       sens=tp / (tp + fn), spec=tn / (tn + fp), kappa=(po - pe) / (1 - pe),
                       flips=int(fp + fn), up=int(fp), down=int(fn),
                       med_minutes_ref=float(np.median(ref)), med_minutes_pipe=float(np.median(pip)),
                       mean_diff=float(diff.mean()), loa_lo=float(diff.mean() - 1.96 * diff.std()),
                       loa_hi=float(diff.mean() + 1.96 * diff.std()))
            for a, b in bands:
                m = (ref >= a) & (ref < b)
                row[f'flips_ref_{int(a)}_{int(min(b, 99))}'] = int(((rb != pb) & m).sum())
            rows.append(row)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, 'o3_misclassification.csv'), index=False)

    # ---- O6 episodes
    e = pd.read_pickle(os.path.join(CACHE, 'episodes.pkl'))
    e = e[e.caseid.isin(c.index)].copy()
    e['cls'] = np.where(e.art_frac >= 0.5, 'flagged',
                        np.where(e.art_frac + e.guard_frac >= 0.5, 'guard', 'physiological'))
    e['flag'] = (e.cls == 'flagged').astype(int)
    e['dur_bin'] = pd.cut(e.dur_s, [0, 10, 30, 60, 120, 300, 1e9],
                          labels=['<=10 s', '11-30 s', '31-60 s', '1-2 min', '2-5 min', '>5 min'])
    e['nadir_bin'] = pd.cut(e.nadir, [-1e9, 20, 40, 55, 65],
                            labels=['<20', '20-39', '40-54', '55-64'], right=False)
    S['o6_episodes'] = dict(n=len(e), cls=e.cls.value_counts().to_dict(),
                            patients=int(e.caseid.nunique()),
                            minutes_by_cls=(e.groupby('cls').dur_s.sum() / 60).to_dict())
    tab = []
    for (db, nb), g in e.groupby(['dur_bin', 'nadir_bin'], observed=False):
        p, lo, hi = wilson(g.flag.sum(), len(g))
        if len(g):
            gg = g.groupby('caseid').agg(k=('flag', 'sum'), n=('flag', 'size'))
            idx = rng.integers(0, len(gg), (B, len(gg)))
            bs = gg.k.to_numpy()[idx].sum(1) / np.maximum(gg.n.to_numpy()[idx].sum(1), 1)
            lo, hi = np.percentile(bs, [2.5, 97.5])
        tab.append(dict(duration=db, nadir=nb, episodes=len(g), flagged=int(g.flag.sum()),
                        guard=int((g.cls == 'guard').sum()), p_flagged=p, lo=lo, hi=hi,
                        patients=int(g.caseid.nunique())))
    pd.DataFrame(tab).to_csv(os.path.join(OUT, 'o6_probability_table.csv'), index=False)
    # duration-only and nadir-only margins
    marg = []
    for col in ('dur_bin', 'nadir_bin'):
        for k, g in e.groupby(col, observed=False):
            p, lo, hi = wilson(g.flag.sum(), len(g))
            marg.append(dict(margin=col, level=k, episodes=len(g), p_flagged=p, lo=lo, hi=hi,
                             minutes=g.dur_s.sum() / 60,
                             flagged_minutes=g.dur_s[g.flag == 1].sum() / 60))
    pd.DataFrame(marg).to_csv(os.path.join(OUT, 'o6_margins.csv'), index=False)

    # rule: depth <= 2 tree, leaves "flagged" only at >= 90% specificity, derived on half
    subj = c.subjectid.to_dict()
    e['half'] = [int(hashlib.sha256(str(subj[k]).encode()).hexdigest(), 16) % 2 for k in e.caseid]
    e['pre_drop'] = e.pre30_max - e.nadir
    feats = {'dur_s': [10, 20, 30, 60, 120], 'nadir': [20, 30, 40, 50],
             'pre_drop': [20, 30, 40, 60, 80]}
    S['o6_rule'] = derive_rule(e, feats)

    # ---- V3 physiological checks
    nb = e[e.nibp_near.notna()]
    v3 = {}
    for k, g in nb.groupby('cls'):
        p, lo, hi = wilson((g.nibp_near >= 70).sum(), len(g))
        v3[k] = dict(n=len(g), p_nibp_ge70=p, lo=lo, hi=hi, nibp_median=float(g.nibp_near.median()))
    S['v3_nibp'] = v3
    # post-unblinding (review): cuff value within +/-60 s, overall and among deep episodes only
    for tag, sub in [('v3_nibp60', e), ('v3_nibp60_nadir_lt40', e[e.nadir < 40])]:
        g0 = sub[sub.nibp_near60.notna()]
        out = {}
        for k, g in g0.groupby('cls'):
            p, lo, hi = wilson((g.nibp_near60 >= 70).sum(), len(g))
            out[k] = dict(n=len(g), p_nibp_ge70=p, lo=lo, hi=hi, nibp_median=float(g.nibp_near60.median()))
        S[tag] = out
    S['v3_nonpuls_ecg'] = dict(windows=int(c.nonpuls_n.sum()),
                               ecg_ok=float(c.nonpuls_ecg_ok.sum() / c.nonpuls_n.sum()),
                               pleth_ok=float(c.nonpuls_pleth_ok.sum() / c.nonpuls_n.sum()))
    af = c.preop_ecg.fillna('').str.contains('Atrial fibrillation')
    S['v3_af'] = dict(n_af=int(af.sum()), nonpuls_af=float(c.frac_nonpulsatile[af].mean()),
                      nonpuls_sinus=float(c.frac_nonpulsatile[~af].mean()),
                      nonpuls_af_median=float(c.frac_nonpulsatile[af].median()),
                      nonpuls_sinus_median=float(c.frac_nonpulsatile[~af].median()))
    # ---- C3 NIBP cuff
    cc = c[c.nibp_events > 0]
    from scipy.stats import wilcoxon
    d = (cc.art_pre_nibp - cc.art_else).dropna()
    S['c3_nibp'] = dict(cases=len(cc), events=int(cc.nibp_events.sum()),
                        art_pre_nibp_mean=float(cc.art_pre_nibp.mean()),
                        art_else_mean=float(cc.art_else.mean()),
                        ratio=float(cc.art_pre_nibp.mean() / cc.art_else.mean()),
                        wilcoxon_p=float(wilcoxon(d).pvalue) if len(d) > 10 else None)
    with open(os.path.join(OUT, 'summary.json'), 'w') as fh:
        json.dump(S, fh, indent=1, default=str)
    e.to_pickle(os.path.join(OUT, 'episodes_labelled.pkl'))
    print(json.dumps({k: S[k] for k in ('n_cases', 'o1_time_fraction', 'o6_episodes', 'o6_rule', 'v3_nibp', 'v3_nibp60', 'v3_nibp60_nadir_lt40', 'v3_nonpuls_ecg', 'v3_af', 'c3_nibp')}, indent=1, default=str))
    print(o2t[['res', 'filter', 'low_min', 'spurious_frac', 'lo', 'hi', 'indeterminate_frac', 'masked_per_low']].round(4).to_string())


def derive_rule(e, feats):
    """Exhaustive depth-<=2 rule: (f1 op t1) [and (f2 op t2)] => flagged.
    Maximise sensitivity on the derivation half subject to specificity >= 0.90."""
    der, val = e[e.half == 0], e[e.half == 1]
    yd = der.flag.to_numpy(bool)
    best = None
    conds = []
    for f, ts in feats.items():
        for t in ts:
            conds.append((f, '<=', t))
            conds.append((f, '>', t))
    def mask(df, cond):
        f, op, t = cond
        x = df[f].to_numpy()
        with np.errstate(invalid='ignore'):
            return (x <= t) if op == '<=' else (x > t)
    cands = [(a,) for a in conds] + [(a, b) for i, a in enumerate(conds) for b in conds[i + 1:] if a[0] != b[0]]
    for cand in cands:
        m = np.ones(len(der), bool)
        for cd in cand:
            m &= mask(der, cd)
        tp, fp = (m & yd).sum(), (m & ~yd).sum()
        spec = 1 - fp / max((~yd).sum(), 1)
        sens = tp / max(yd.sum(), 1)
        if spec >= 0.90 and (best is None or sens > best[1] or (sens == best[1] and len(cand) < len(best[0]))):
            best = (cand, sens, spec)
    if best is None:
        return dict(rule=None)
    m = np.ones(len(val), bool)
    for cd in best[0]:
        m &= mask(val, cd)
    yv = val.flag.to_numpy(bool)
    tp, fp, fn, tn = (m & yv).sum(), (m & ~yv).sum(), (~m & yv).sum(), (~m & ~yv).sum()
    # cluster bootstrap on validation half
    vv = val.assign(m=m, y=yv)
    g = vv.groupby('caseid').apply(lambda d: pd.Series(dict(tp=(d.m & d.y).sum(), fp=(d.m & ~d.y).sum(),
                                                             fn=(~d.m & d.y).sum(), tn=(~d.m & ~d.y).sum())))
    idx = rng.integers(0, len(g), (B, len(g)))
    G = g.to_numpy()[idx].sum(1)
    sens_b = G[:, 0] / (G[:, 0] + G[:, 2])
    spec_b = G[:, 3] / (G[:, 3] + G[:, 1])
    ppv_b = G[:, 0] / np.maximum(G[:, 0] + G[:, 1], 1)
    return dict(rule=' AND '.join(f'{f} {op} {t}' for f, op, t in best[0]),
                derivation=dict(sens=best[1], spec=best[2], n=len(der), flagged=int(yd.sum())),
                validation=dict(n=len(val), flagged=int(yv.sum()), sens=tp / (tp + fn), spec=tn / (tn + fp),
                                ppv=tp / max(tp + fp, 1),
                                sens_ci=list(np.percentile(sens_b, [2.5, 97.5])),
                                spec_ci=list(np.percentile(spec_b, [2.5, 97.5])),
                                ppv_ci=list(np.percentile(ppv_b, [2.5, 97.5]))))


if __name__ == '__main__':
    main()
