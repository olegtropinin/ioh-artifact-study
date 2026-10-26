"""POST HOC statistical analyses requested by the round-1 reviewers (not in the frozen protocol,
except S4 and S6, which were pre-specified but omitted from the original run).

python src/posthoc_stats.py   -> out/posthoc_review/stats.json, tost.json
"""
import json
import os
import sys
from multiprocessing import Pool

import numpy as np
import pandas as pd

sys.argv = [sys.argv[0], 'real'] + sys.argv[1:]
sys.path.insert(0, os.path.dirname(__file__))
import analysis as A                                                         # noqa: E402
from models import cohort, covariates, firth_logit, load_outcome, rcs       # noqa: E402

OUT = os.path.join(A.ROOT, 'out', 'posthoc_review')
N_SIM = int(os.environ.get('N_SIM', 200))
B_SIM = int(os.environ.get('B_SIM', 200))
P_SIM = int(os.environ.get('P_SIM', 200))
ST = {}


def lor(e, Z, y):
    X = np.column_stack([np.ones(len(y)), e, Z])
    X = X[:, np.r_[True, True, np.ptp(X[:, 2:], 0) > 0]]
    return firth_logit(X, y)[0][1]


def ror_ci(c, y, ep, er, B=1000, P=200, seed=0, Z=None):
    """A15 interval for one pipeline/reference pair on an arbitrary analysis set."""
    Z = covariates(c) if Z is None else Z
    hat = lor(ep, Z, y) - lor(er, Z, y)
    rng = np.random.default_rng(seed)
    n = len(y)
    bs = []
    for _ in range(B):
        i = rng.integers(0, n, n)
        bs.append(lor(ep[i], Z[i], y[i]) - lor(er[i], Z[i], y[i]))
    ns = []
    for _ in range(P):
        yy = rng.permutation(y)
        ns.append(lor(ep, Z, yy) - lor(er, Z, yy))
    s = max(np.std(bs, ddof=1), np.std(ns, ddof=1))
    return dict(ror=float(np.exp(hat)), lo=float(np.exp(hat - 1.96 * s)), hi=float(np.exp(hat + 1.96 * s)),
                n=int(n), events=int(y.sum()))


def _sim_init(Z, ep, er, eta, up, down):
    ST.update(Z=Z, ep=ep, er=er, eta=eta, up=up, down=down)


def _sim(args):
    """One simulated dataset under the covariate-conditional DGP; returns the A15 decision."""
    g_up, g_down, seed, B, P = args
    Z, ep, er = ST['Z'], ST['ep'], ST['er']
    rng = np.random.default_rng(seed)
    p = 1 / (1 + np.exp(-(ST['eta'] + g_up * ST['up'] + g_down * ST['down'])))
    y = (rng.random(len(p)) < p).astype(float)
    hat = lor(ep, Z, y) - lor(er, Z, y)
    if B == 0:
        return dict(lror=float(hat))
    n = len(y)
    bs, ns = [], []
    for _ in range(B):
        i = rng.integers(0, n, n)
        bs.append(lor(ep[i], Z[i], y[i]) - lor(er[i], Z[i], y[i]))
    for _ in range(P):
        yy = rng.permutation(y)
        ns.append(lor(ep, Z, yy) - lor(er, Z, yy))
    s = max(np.std(bs, ddof=1), np.std(ns, ddof=1))
    lo, hi = np.exp(hat - 1.96 * s), np.exp(hat + 1.96 * s)
    return dict(lror=float(hat), lo=float(lo), hi=float(hi), equivalent=bool(lo >= 0.8 and hi <= 1.25),
                covers=bool(lo <= np.exp(0) <= hi), k_up=int(y[ST['up'] > 0].sum()), events=int(y.sum()))


def run_sims(pool, g_up, g_down, n, seed0, B=B_SIM, P=P_SIM):
    return pool.map(_sim, [(g_up, g_down, seed0 + i, B, P) for i in range(n)], chunksize=1)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    c, _ = cohort()
    y = load_outcome(c, 'real')
    Z = covariates(c)
    S = {}

    # 1. discordant patients
    disc = {}
    for f, r in [('F1', 'R3'), ('F0', 'R1'), ('F3', 'R2'), ('F6', 'R3')]:
        p = np.mean([A.expo(c, 'pipe', f, r, o, 65, 'binary') for o in A.offsets(r)], 0)
        q = np.mean([A.expo(c, 'ref', 'bridged', r, o, 65, 'binary') for o in A.offsets(r)], 0)
        disc[f'{f}x{r}'] = dict(up=int((p > q).sum()), aki_up=int(y[p > q].sum()),
                                down=int((p < q).sum()), aki_down=int(y[p < q].sum()))
    ep = A.expo(c, 'pipe', 'F1', 'R3', 0, 65, 'binary')
    er = A.expo(c, 'ref', 'bridged', 'R3', 0, 65, 'binary')
    up, down = (ep > er).astype(float), (ep < er).astype(float)
    X = np.column_stack([np.ones(len(y)), er, Z])
    beta = firth_logit(X, y)[0]
    eta = X @ beta
    pr = 1 / (1 + np.exp(-eta))
    dd = (up + down) > 0
    pd_ = pr[dd]
    # Poisson-binomial P(k = 0) among discordant
    disc['F1xR3_expected_aki'] = float(pd_.sum())
    disc['F1xR3_p_k0'] = float(np.prod(1 - pd_))
    # ROR as a function of k AKI cases among the up-flipped (swap with concordant cases)
    rng = np.random.default_rng(5)
    conc_cases = np.flatnonzero((~dd) & (y == 1))
    upi = np.flatnonzero(up > 0)
    curve = {}
    for k in range(0, 6):
        vals = []
        for _ in range(30 if k else 1):
            yy = y.copy()
            if k:
                yy[rng.choice(upi, k, replace=False)] = 1
                yy[rng.choice(conc_cases, k, replace=False)] = 0
            vals.append(np.exp(lor(ep, Z, yy) - lor(er, Z, yy)))
        curve[k] = float(np.mean(vals))
    disc['F1xR3_ror_by_k_up_cases'] = curve
    S['discordant'] = disc
    print('discordant', json.dumps(disc))

    # 2. split-sample calibrated coverage (archived): SD from the permuted dry run's own null
    cal = json.load(open(os.path.join(A.ROOT, 'out', 'null_calibration.json')))
    pm = np.load(os.path.join(A.ROOT, 'out', 'results_permuted', 'perm_null_main.npy'))
    names = [f'ref@{r}' for r in A.RES] + [f'{f}x{r}' for f in A.FILTERS for r in A.RES]
    j = {n: i for i, n in enumerate(names)}
    cov = {}
    for k in cal['summary']:
        f, r = k.split('x')
        sd_ind = float(np.std(pm[:, j[k]] - pm[:, j['ref@' + r]], ddof=1))
        L = np.array([run[k]['lror'] for run in cal['runs']])
        se = np.array([run[k]['se'] for run in cal['runs']])
        s = np.maximum(se, sd_ind)
        cov[k] = dict(null_sd_independent=sd_ind, coverage=float(np.mean(np.abs(L) <= 1.96 * s)), n=len(L))
    S['calibrated_coverage_independent'] = cov
    print('coverage', json.dumps(cov))

    # 3. sensitivity analyses: pre-specified S4/S6 (omitted originally) and review-requested ones
    sens = {}
    c4, _ = cohort(skip=('creatinine within 7 days after surgery',))
    y4 = c4.aki.fillna(0).to_numpy(float)
    sens['S4 missing postoperative creatinine = no AKI (pre-specified)'] = ror_ci(
        c4, y4, A.expo(c4, 'pipe', 'F1', 'R3', 0, 65, 'binary'), A.expo(c4, 'ref', 'bridged', 'R3', 0, 65, 'binary'), seed=41)
    c6, _ = cohort(skip=('not transplantation',))
    y6 = c6.aki.to_numpy(float)
    sens['S6 transplantation included (pre-specified)'] = ror_ci(
        c6, y6, A.expo(c6, 'pipe', 'F1', 'R3', 0, 65, 'binary'), A.expo(c6, 'ref', 'bridged', 'R3', 0, 65, 'binary'), seed=61)
    cg = c[c.department != 'Gynecology']
    yg = load_outcome(cg, 'real')
    sens['without gynaecology (low creatinine testing)'] = ror_ci(
        cg, yg, A.expo(cg, 'pipe', 'F1', 'R3', 0, 65, 'binary'), A.expo(cg, 'ref', 'bridged', 'R3', 0, 65, 'binary'), seed=71)
    # disease risk score: logistic model of AKI on the full adjustment set without exposure
    Xd = np.column_stack([np.ones(len(y)), Z])
    drs = Xd @ firth_logit(Xd, y)[0]
    kn = np.percentile(drs, [10, 50, 90])
    Zd = np.column_stack([drs, rcs(drs, kn)])
    sens['disease risk score, 2 df'] = ror_ci(c, y, ep, er, seed=81, Z=Zd)
    for v in ['concord', 'valid25_obs', 'valid75_obs']:
        sens[f'reference={v}'] = ror_ci(c, y, ep, A.expo(c, 'ref', v, 'R3', 0, 65, 'binary'), seed=91)
    S['sensitivity'] = sens
    print('sens', json.dumps(sens, indent=1))
    S['epv_full'] = float(y.sum() / (Z.shape[1] + 1))
    desc = pd.read_pickle(os.path.join(A.CACHE, 'desc.pkl')).set_index('caseid').reindex(A.descriptive_cohort().index)
    S['monitor_waveform_discordance'] = dict(mean=float(desc.disc_frac.mean()), median=float(desc.disc_frac.median()),
                                             p90=float(desc.disc_frac.quantile(.9)))
    S['lag_s'] = {int(k): int(v) for k, v in (desc.lag * 2).value_counts().sort_index().items()}

    # 4. fragility summaries and simultaneous-band equivalence (from the frozen outputs)
    fr = pd.read_csv(os.path.join(A.ROOT, 'out', 'results_real', 'ror_binary_FxR.csv'))
    S['equivalent_pointwise'] = int(((fr.ror_lo >= 0.8) & (fr.ror_hi <= 1.25)).sum())
    S['equivalent_simultaneous'] = int(((fr.ror_simlo >= 0.8) & (fr.ror_simhi <= 1.25)).sum())
    S['borderline_cells'] = fr[(np.abs(fr.ror_hi - 1.25) < 0.01) | (np.abs(fr.ror_lo - 0.8) < 0.01)][
        ['filter', 'res', 'ror', 'ror_lo', 'ror_hi']].round(4).to_dict('records')
    sc = pd.read_csv(os.path.join(A.ROOT, 'out', 'results_real', 'spec_curve.csv'))
    sig = lambda d: (d.lo > 1) | (d.hi < 1)
    ref = sc[sc.family == 'ref'].set_index(['metric', 'thr', 'res'])
    pp = sc[sc.family == 'pipe'].copy()
    pp['ref_sig'] = [sig(ref.loc[(m, t, r)]) for m, t, r in zip(pp.metric, pp.thr, pp.res)]
    pp['sig'] = sig(pp)
    S['fragility'] = dict(pipe_ci_excludes_1=int(pp.sig.sum()), n=len(pp),
                          ref_ci_excludes_1=int(sig(sc[sc.family == 'ref']).sum()),
                          significance_flips=int((pp.sig != pp.ref_sig).sum()),
                          flips_by_metric=pp[pp.sig != pp.ref_sig].metric.value_counts().to_dict())
    print('fragility', S['fragility'], S['equivalent_pointwise'], S['equivalent_simultaneous'])

    # 5. O5 negative control in its own model, and per-unit odds ratios
    o2 = pd.read_pickle(os.path.join(A.CACHE, 'o2.pkl'))
    q = o2[(o2.res == 'R1') & (o2['filter'] == 'F0')].set_index('caseid').reindex(c.index)
    hours = c.ref_monitored / 60
    refmin = A.raw('ref', 'bridged', 'R1', 0, 65, 'minutes').reindex(c.index).to_numpy(float)
    kn = np.percentile(refmin, [10, 50, 90])
    base = np.column_stack([np.minimum(refmin, 120) / 10, rcs(refmin, kn) / 100, np.log(hours)])
    o5 = {}
    for name, v in [('spurious_hypo', q.spurious / hours), ('spurious_hyper_negative_control', q.spurious_hyper / hours)]:
        e = np.log1p(np.asarray(v, float))
        Xm = np.column_stack([np.ones(len(y)), e, base, Z])
        b, cv, _ = firth_logit(Xm, y)
        se = np.sqrt(cv[1, 1])
        o5[name] = dict(or_per_log1p=float(np.exp(b[1])), lo=float(np.exp(b[1] - 1.96 * se)),
                        hi=float(np.exp(b[1] + 1.96 * se)), sd=float(e.std()),
                        or_per_sd=float(np.exp(b[1] * e.std())), lo_sd=float(np.exp((b[1] - 1.96 * se) * e.std())),
                        hi_sd=float(np.exp((b[1] + 1.96 * se) * e.std())))
    S['o5_separate_models_F0xR1'] = o5
    with open(os.path.join(OUT, 'stats.json'), 'w') as fh:
        json.dump(S, fh, indent=1, default=float)

    # 6. operating characteristics of the A15 equivalence decision at the margins (TOST check)
    T = {}
    with Pool(int(os.environ.get('NPROC', 10)), initializer=_sim_init, initargs=(Z, ep, er, eta, up, down)) as pool:
        grid = {}
        for g in (0.0, 1.0, 2.0, 3.0, 4.0):
            res = run_sims(pool, g, 0.0, 60, 900000 + int(g * 1000), B=0, P=0)
            grid[f'up{g}'] = float(np.exp(np.median([x['lror'] for x in res])))
        for g in (2.0, 4.0, 8.0):
            res = run_sims(pool, 0.0, g, 60, 950000 + int(g * 1000), B=0, P=0)
            grid[f'down{g}'] = float(np.exp(np.median([x['lror'] for x in res])))
        T['median_ror_by_gamma'] = grid
        print('gamma grid', grid)
        ups = [(float(k[2:]), v) for k, v in grid.items() if k.startswith('up')]
        g125 = float(np.interp(np.log(1.25), [np.log(v) for _, v in ups], [g for g, _ in ups]))
        for tag, gu in [('null', 0.0), ('upper_margin', g125)]:
            res = run_sims(pool, gu, 0.0, N_SIM, 990000 + int(gu * 1000))
            L = np.array([x['lror'] for x in res])
            T[tag] = dict(gamma_up=gu, median_ror=float(np.exp(np.median(L))),
                          p_equivalent=float(np.mean([x['equivalent'] for x in res])),
                          coverage_of_1=float(np.mean([x['covers'] for x in res])),
                          sd_lror=float(L.std(ddof=1)), n=len(res))
            print(tag, T[tag])
    T['lower_margin'] = 'not reachable: with 5 down-flipped patients the median ROR stays above 0.80 even when all are cases' \
        if min(v for k, v in grid.items() if k.startswith('down')) > 0.8 else 'reachable; not simulated'
    with open(os.path.join(OUT, 'tost.json'), 'w') as fh:
        json.dump(T, fh, indent=1, default=float)
    print(json.dumps(T, indent=1))
