"""All pre-specified analyses. Usage: python src/analysis.py permuted|real

Writes out/results_<mode>/*.csv and a JSON summary. In 'permuted' mode every outcome is
a seeded permutation, so the run exercises the code without revealing any association.
"""
import json
import os
import sys
import numpy as np
import pandas as pd
from multiprocessing import Pool
from scipy.stats import spearmanr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models import (cohort, load_outcome, fit_exposure, firth_logit, covariates, rcs,
                    code_hash, ROOT, CACHE)
from pipelines import FILTERS, RES

MODE = sys.argv[1] if len(sys.argv) > 1 else 'permuted'
OUT = os.path.join(ROOT, 'out', f'results_{MODE}')
B_MAIN = int(os.environ.get('B_MAIN', 2000))
B_SENS = int(os.environ.get('B_SENS', 1000))
NPROC = int(os.environ.get('NPROC', 12))
METRICS = ['binary', 'minutes', 'auc', 'twa']

X = pd.read_pickle(os.path.join(CACHE, 'exposures.pkl'))
X['key'] = list(zip(X.family, X['filter'], X.res, X.offset, X.thr))
WIDE = {m: X.pivot_table(index='caseid', columns='key', values=m) for m in ('minutes', 'auc', 'twa')}


def raw(family, filt, res, off, thr, metric):
    src = 'minutes' if metric == 'binary' else metric
    return WIDE[src][(family, filt, res, off, thr)]


def transform(v, metric, cap=None):
    v = v.to_numpy(float)
    if metric == 'binary':
        return (v >= 10).astype(float)
    if metric == 'minutes':
        return np.minimum(v, 120) / 10
    if metric == 'auc':
        return np.minimum(v, cap) / 100
    return v


def expo(c, family, filt, res, off, thr, metric):
    cap = None
    if metric == 'auc':
        cap = np.nanpercentile(raw('ref', 'bridged', res, off, thr, 'auc').reindex(c.index), 99)
    return transform(raw(family, filt, res, off, thr, metric).reindex(c.index), metric, cap)


def offsets(res):
    return RES[res]


# ---------------------------------------------------------------- bootstrap worker

STATE = {}


def _init(c, y, specs):
    STATE.update(c=c, y=y, specs=specs)


def _boot(seed):
    c, y, specs = STATE['c'], STATE['y'], STATE['specs']
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(c), len(c)) if seed >= 0 else np.arange(len(c))
    cc, yy = c.iloc[idx], y[idx]
    out, fails = [], 0
    for name, cols in specs:        # each spec: list of (exposure arrays) -> mean log-OR
        bs = []
        for e in cols:
            b, se, ok = fit_exposure(e[idx], cc, yy)
            fails += (not ok)
            bs.append(b)
        out.append(np.mean(bs))
    return np.array(out), fails


def bootstrap(c, y, specs, B, seed0):
    with Pool(NPROC, initializer=_init, initargs=(c, y, specs)) as p:
        res = p.map(_boot, [-1] + [seed0 + i for i in range(B)], chunksize=max(1, B // (NPROC * 4)))
    est = res[0][0]
    boots = np.array([r[0] for r in res[1:]])
    fails = sum(r[1] for r in res)
    return est, boots, fails


def spec_cols(c, family, filt, res, thr, metric):
    return [expo(c, family, filt, res, o, thr, metric) for o in offsets(res)]


# ---------------------------------------------------------------- main

def main():
    os.makedirs(OUT, exist_ok=True)
    c, flow = cohort()
    y = load_outcome(c, MODE)
    summary = dict(mode=MODE, code_sha256=code_hash(), n=len(c), events=int(y.sum()),
                   flow=flow)
    pd.DataFrame(flow, columns=['step', 'n']).to_csv(os.path.join(OUT, 'flow.csv'), index=False)

    # ---- primary + 35 F x R binary RORs (T = 65) with one paired bootstrap
    specs = [('ref@' + r, spec_cols(c, 'ref', 'bridged', r, 65, 'binary')) for r in RES]
    specs += [(f'{f}x{r}', spec_cols(c, 'pipe', f, r, 65, 'binary')) for f in FILTERS for r in RES]
    names = [s[0] for s in specs]
    est, boots, fails = bootstrap(c, y, specs, B_MAIN, 1000)
    np.save(os.path.join(OUT, 'boot_main.npy'), boots)
    j = {n: i for i, n in enumerate(names)}
    rows = []
    lror_hat, lror_b = [], []
    for f in FILTERS:
        for r in RES:
            a, b = j[f'{f}x{r}'], j['ref@' + r]
            lror_hat.append(est[a] - est[b])
            lror_b.append(boots[:, a] - boots[:, b])
    lror_hat, lror_b = np.array(lror_hat), np.array(lror_b).T
    se = lror_b.std(0, ddof=1)
    zmax = np.max(np.abs(lror_b - lror_hat) / se, 1)
    crit = np.percentile(zmax, 95)
    k = 0
    for f in FILTERS:
        for r in RES:
            lo, hi = np.percentile(lror_b[:, k], [2.5, 97.5])
            rows.append(dict(filter=f, res=r, or_pipe=np.exp(est[j[f'{f}x{r}']]),
                             or_ref=np.exp(est[j['ref@' + r]]), ror=np.exp(lror_hat[k]),
                             ror_lo=np.exp(lo), ror_hi=np.exp(hi),
                             ror_simlo=np.exp(lror_hat[k] - crit * se[k]),
                             ror_simhi=np.exp(lror_hat[k] + crit * se[k])))
            k += 1
    fr = pd.DataFrame(rows)
    fr.to_csv(os.path.join(OUT, 'ror_binary_FxR.csv'), index=False)
    prim = fr[(fr['filter'] == 'F1') & (fr.res == 'R3')].iloc[0]
    if prim.ror_lo >= 0.80 and prim.ror_hi <= 1.25:
        verdict = 'equivalent'
    elif (prim.ror_lo > 1 or prim.ror_hi < 1) and not (0.80 <= prim.ror <= 1.25):
        verdict = 'material change'
    else:
        verdict = 'inconclusive'
    summary['primary'] = dict(prim.to_dict(), verdict=verdict, bootstrap_fails=int(fails),
                              B=B_MAIN, simultaneous_crit=float(crit))
    # resolution effect: OR(ref@R)/OR(ref@R3)
    summary['resolution_effect'] = {
        r: dict(ratio=float(np.exp(est[j['ref@' + r]] - est[j['ref@R3']])),
                lo=float(np.exp(np.percentile(boots[:, j['ref@' + r]] - boots[:, j['ref@R3']], 2.5))),
                hi=float(np.exp(np.percentile(boots[:, j['ref@' + r]] - boots[:, j['ref@R3']], 97.5))))
        for r in RES}

    # ---- key secondary (b): minutes per 10, F1xR3 vs ref@R3
    specs_b = [('ref', spec_cols(c, 'ref', 'bridged', 'R3', 65, 'minutes')),
               ('pipe', spec_cols(c, 'pipe', 'F1', 'R3', 65, 'minutes')),
               ('ref_R1', spec_cols(c, 'ref', 'bridged', 'R1', 65, 'minutes')),
               ('pipe_F0R1', spec_cols(c, 'pipe', 'F0', 'R1', 65, 'minutes'))]
    eb, bb, fb = bootstrap(c, y, specs_b, B_SENS, 50000)
    summary['dose_slope'] = dict(
        beta_ref=float(eb[0]), beta_pipe=float(eb[1]),
        or10_ref=float(np.exp(eb[0])), or10_pipe=float(np.exp(eb[1])),
        diff=float(eb[1] - eb[0]), diff_ci=list(map(float, np.percentile(bb[:, 1] - bb[:, 0], [2.5, 97.5]))),
        attenuation=float(eb[1] / eb[0]) if eb[0] != 0 else None,
        F0R1_or10=float(np.exp(eb[3])), refR1_or10=float(np.exp(eb[2])),
        F0R1_diff_ci=list(map(float, np.percentile(bb[:, 3] - bb[:, 2], [2.5, 97.5]))), fails=int(fb))

    # ---- specification curve: all metrics x thresholds x F x R (point estimates, Wald CI)
    sc = []
    for metric in METRICS:
        for thr in (55, 60, 65):
            refb = {}
            for r in RES:
                bs = [fit_exposure(e, c, y) for e in spec_cols(c, 'ref', 'bridged', r, thr, metric)]
                refb[r] = np.mean([b[0] for b in bs])
                sc.append(dict(metric=metric, thr=thr, family='ref', filter='bridged', res=r,
                               logor=refb[r], se=np.mean([b[1] for b in bs])))
            for f in FILTERS:
                for r in RES:
                    bs = [fit_exposure(e, c, y) for e in spec_cols(c, 'pipe', f, r, thr, metric)]
                    lo = np.mean([b[0] for b in bs])
                    sc.append(dict(metric=metric, thr=thr, family='pipe', filter=f, res=r,
                                   logor=lo, se=np.mean([b[1] for b in bs]),
                                   lror=lo - refb[r]))
    sc = pd.DataFrame(sc)
    sc['or'] = np.exp(sc.logor)
    sc['lo'] = np.exp(sc.logor - 1.96 * sc.se)
    sc['hi'] = np.exp(sc.logor + 1.96 * sc.se)
    sc['ror'] = np.exp(sc.lror)
    sc.to_csv(os.path.join(OUT, 'spec_curve.csv'), index=False)
    pp = sc[sc.family == 'pipe']
    summary['spec_curve'] = dict(
        n_specs=int(len(pp)), ci_excludes_1=int(((pp.lo > 1) | (pp.hi < 1)).sum()),
        ror_median=float(pp.ror.median()), ror_iqr=list(map(float, pp.ror.quantile([.25, .75]))),
        ror_range=[float(pp.ror.min()), float(pp.ror.max())])

    # ---- sensitivity analyses on the primary contrast (binary, T65, F1xR3)
    sens = []
    pipe_col = spec_cols(c, 'pipe', 'F1', 'R3', 65, 'binary')
    for v in ['unbridged', 'guard0', 'guard30', 'pp5', 'pp12', 'valid25', 'valid75', 'wavemean']:
        specs_s = [('pipe', pipe_col), ('ref', [expo(c, 'ref', v, 'R3', 0, 65, 'binary')])]
        es, bs_, _ = bootstrap(c, y, specs_s, B_SENS, 90000)
        d = bs_[:, 0] - bs_[:, 1]
        sens.append(dict(analysis=f'reference={v}', ror=np.exp(es[0] - es[1]),
                         lo=np.exp(np.percentile(d, 2.5)), hi=np.exp(np.percentile(d, 97.5))))
    # S10: numerics-defined period for the pipeline
    cc = c[c.index.isin(WIDE['minutes'].index[WIDE['minutes'][('pipe_numper', 'F1', 'R3', 0, 65)].notna()])]
    yy = load_outcome(c, MODE)[np.isin(c.index, cc.index)]
    specs_s = [('pipe', [expo(cc, 'pipe_numper', 'F1', 'R3', 0, 65, 'binary')]),
               ('ref', [expo(cc, 'ref', 'bridged', 'R3', 0, 65, 'binary')])]
    es, bs_, _ = bootstrap(cc, yy, specs_s, B_SENS, 91000)
    d = bs_[:, 0] - bs_[:, 1]
    sens.append(dict(analysis='S10 numerics-defined period', ror=np.exp(es[0] - es[1]),
                     lo=np.exp(np.percentile(d, 2.5)), hi=np.exp(np.percentile(d, 97.5))))
    # outcome / adjustment variants: point estimates of ROR with Wald SE of each OR
    def ror_point(cx, yx, reduced=False, extra=None):
        ep = expo(cx, 'pipe', 'F1', 'R3', 0, 65, 'binary')
        er = expo(cx, 'ref', 'bridged', 'R3', 0, 65, 'binary')
        if extra is not None:
            cx = cx.copy()
            cx['__extra'] = extra
        bp = fit_exposure(ep, cx, yx, reduced)
        br = fit_exposure(er, cx, yx, reduced)
        return np.exp(bp[0]), np.exp(br[0]), np.exp(bp[0] - br[0])
    for name, fn in [('S5 + blood loss', 'ebl'), ('S11 + number of postoperative creatinines', 'ncr')]:
        cx = c.copy()
        extra = (np.log1p(cx.intraop_ebl.fillna(cx.intraop_ebl.median())) if fn == 'ebl'
                 else cx.n_cr_post7d.fillna(0)).to_numpy(float)
        ep = expo(cx, 'pipe', 'F1', 'R3', 0, 65, 'binary')
        er = expo(cx, 'ref', 'bridged', 'R3', 0, 65, 'binary')
        Z = covariates(cx)
        res_ = []
        for e in (ep, er):
            Xm = np.column_stack([np.ones(len(cx)), e, Z, extra])
            b, cov, ok = firth_logit(Xm, y)
            res_.append(b[1])
        sens.append(dict(analysis=name, or_pipe=np.exp(res_[0]), or_ref=np.exp(res_[1]),
                         ror=np.exp(res_[0] - res_[1])))
    # S7: AKI stage >= 2, reduced set
    y2 = load_outcome(c.assign(aki2=(c.aki_stage >= 2).astype(float)), MODE, 'aki2')
    o = ror_point(c, y2, reduced=True)
    sens.append(dict(analysis='S7 AKI stage >= 2 (reduced set)', or_pipe=o[0], or_ref=o[1], ror=o[2],
                     events=int(y2.sum())))
    pd.DataFrame(sens).to_csv(os.path.join(OUT, 'sensitivity.csv'), index=False)
    summary['sensitivity'] = sens

    # ---- O5 differential misclassification
    o2 = pd.read_pickle(os.path.join(CACHE, 'o2.pkl'))
    q = o2[(o2.res == 'R3') & (o2['filter'] == 'F1')].set_index('caseid').reindex(c.index)
    hours = c.ref_monitored / 60
    labs = pd.read_csv(os.path.join(ROOT, 'data', 'labs.csv.gz'))
    ph = labs[labs.name == 'ph'].merge(c[['anestart', 'aneend']].reset_index(), on='caseid')
    abg = ph[(ph.dt >= ph.anestart) & (ph.dt <= ph.aneend)].groupby('caseid').size()
    abg_h = abg.reindex(c.index).fillna(0) / hours
    attrib = q.spurious / hours
    rho1 = spearmanr(attrib, abg_h, nan_policy='omit')
    rho2 = spearmanr(attrib, c.asa, nan_policy='omit')
    refmin = raw('ref', 'bridged', 'R3', 0, 65, 'minutes').reindex(c.index).to_numpy(float)
    kn = np.percentile(refmin, [10, 50, 90])
    if kn[0] == kn[1]:
        kn = np.percentile(refmin[refmin > 0], [10, 50, 90])
    base = np.column_stack([np.minimum(refmin, 120) / 10, rcs(refmin, kn) / 100, np.log(hours)])
    Z = covariates(c)
    o5 = {}
    for name, cols in [('b_g1_zero_high', [np.log1p(q.spur_g1 / hours)]),
                       ('b_g2_nonpuls_noise', [np.log1p(q.spur_g2 / hours)]),
                       ('b_all', [np.log1p(attrib)]),
                       ('c_negative_control', [np.log1p(attrib), np.log1p(q.spurious_hyper / hours)]),
                       ('d_mechanism', [np.log1p(attrib), abg_h,
                                        np.log1p(c.intraop_ebl.fillna(c.intraop_ebl.median())),
                                        c.intraop_rbc.fillna(0)])]:
        E = np.column_stack([np.asarray(v, float) for v in cols])
        Xm = np.column_stack([np.ones(len(c)), E, base, Z])
        b, cov, ok = firth_logit(Xm, y)
        se = np.sqrt(np.diag(cov))
        o5[name] = [dict(coef=float(b[1 + i]), or_per_log1p=float(np.exp(b[1 + i])),
                         lo=float(np.exp(b[1 + i] - 1.96 * se[1 + i])),
                         hi=float(np.exp(b[1 + i] + 1.96 * se[1 + i]))) for i in range(E.shape[1])]
    summary['o5'] = dict(spearman_attrib_abg=[float(rho1.statistic), float(rho1.pvalue)],
                         spearman_attrib_asa=[float(rho2.statistic), float(rho2.pvalue)],
                         abg_per_h_median=float(abg_h.median()), models=o5,
                         attrib_nonzero=int((q.spurious > 0).sum()))

    # ---- mortality: one specification, reduced set (descriptive cohort, non-transplant)
    summary['mortality'] = mortality()

    summary['finished'] = True
    with open(os.path.join(OUT, 'summary.json'), 'w') as fh:
        json.dump(summary, fh, indent=1, default=float)
    print(json.dumps({k: summary[k] for k in ('n', 'events', 'primary', 'spec_curve')}, indent=1, default=float))


def descriptive_cohort():
    c = pd.read_pickle(os.path.join(ROOT, 'data', 'cohort_raw.pkl')).set_index('caseid')
    desc = pd.read_pickle(os.path.join(CACHE, 'desc.pkl')).set_index('caseid')
    x = pd.read_pickle(os.path.join(CACHE, 'exposures.pkl'))
    refmon = x[(x.family == 'ref') & (x['filter'] == 'bridged') & (x.res == 'R3')
               & (x.thr == 65)].set_index('caseid').monitored
    c = c.join(desc, how='inner').join(refmon.rename('ref_monitored'), how='inner')
    c = c[(c.age >= 18) & (c.ane_type == 'General') & (c.ref_monitored >= 30)].sort_index()
    c = c[~c.subjectid.duplicated(keep='first')]
    c['asa3'] = (c.asa >= 3).astype(float)
    c['log_dur'] = np.log(c.ane_dur_h.clip(lower=0.25))
    return c


def mortality():
    c = descriptive_cohort()
    c = c[(c.optype != 'Transplantation') & c.egfr.notna()]
    y = load_outcome(c, MODE, 'death_inhosp')
    ep = expo(c, 'pipe', 'F1', 'R3', 0, 65, 'binary')
    er = expo(c, 'ref', 'bridged', 'R3', 0, 65, 'binary')
    bp, sp, _ = fit_exposure(ep, c, y, reduced=True)
    br, sr, _ = fit_exposure(er, c, y, reduced=True)
    return dict(n=len(c), deaths=int(y.sum()), or_pipe=float(np.exp(bp)),
                or_pipe_ci=[float(np.exp(bp - 1.96 * sp)), float(np.exp(bp + 1.96 * sp))],
                or_ref=float(np.exp(br)),
                or_ref_ci=[float(np.exp(br - 1.96 * sr)), float(np.exp(br + 1.96 * sr))],
                ror=float(np.exp(bp - br)))


if __name__ == '__main__':
    main()
