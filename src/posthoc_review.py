"""POST HOC analyses requested by the round-1 reviewers (not in the frozen protocol).

1. Peri-cuff artefact by subtype, for regular (automatic-cycle) versus irregular cuff readings,
   and by surgical position.
2. Real-time view of episodes: P(flagged | still below 65 mmHg at elapsed time t, nadir so far).
3. Independent pulse during deep flagged episodes: plethysmographic and ECG heart rate.
4. Time from anaesthesia start to the start of arterial monitoring.

python src/posthoc_review.py   -> out/posthoc_review/*.csv, summary.json
"""
import json
import os
import sys
from multiprocessing import Pool

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from artifact import ARTEFACT, classify, runs          # noqa: E402
from pipelines import best_lag, first_last_run, shift  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'out', 'posthoc_review')
CASES = pd.read_pickle(os.path.join(ROOT, 'data', 'cohort_raw.pkl')).set_index('caseid')
LABS = ['valid', 'missing', 'zero', 'high', 'nonpulsatile', 'noise', 'guard']
ELAPSED = (10, 30, 60, 120)


def one(path):
    cid = int(os.path.basename(path)[:-4])
    if cid not in CASES.index:
        return None
    d = dict(np.load(path))
    lab0 = classify(d)
    lag = best_lag(d, lab0)
    a0 = int(max(0, CASES.anestart[cid]) // 2)
    a1 = int(min(len(lab0), CASES.aneend[cid] // 2))
    per = first_last_run(lab0 == 0, a0, a1)
    if per is None:
        return None
    p0, p1 = per
    sl = slice(p0, p1)
    lab = lab0[sl]
    m = shift(d['n_ART_MBP'], lag)[sl]
    nb = d['n_NIBP_MBP'][sl]          # cuff values are not lag-shifted
    hr = shift(d['n_HR'], lag)[sl]
    ph = shift(d['n_PLETH_HR'], lag)[sl]
    out = dict(caseid=cid, start_delay_min=(p0 - a0) * 2 / 60)

    # 1. cuff readings: subtype composition 30-4 s before each new value
    prev = np.concatenate([[np.nan], nb[:-1]])
    ev = np.flatnonzero(np.isfinite(nb) & ~(prev == nb))
    cuff = []
    if len(ev):
        gaps = np.diff(ev) * 2.0
        mode = None
        if len(gaps) >= 3:
            vals, cnt = np.unique(np.round(gaps / 30) * 30, return_counts=True)
            mode = vals[cnt.argmax()] if cnt.max() >= 3 else None
        for k, j in enumerate(ev):
            w = lab[max(0, j - 15):max(0, j - 2)]
            if len(w) < 5:
                continue
            gap = gaps[k - 1] if k > 0 else np.nan
            regular = mode is not None and np.isfinite(gap) and abs(gap - mode) <= 20
            cuff.append(dict(caseid=cid, regular=bool(regular),
                             **{f'f_{n}': float((w == i).mean()) for i, n in enumerate(LABS)}))
    out['else'] = {n: float((lab == i).mean()) for i, n in enumerate(LABS)}

    # 2-3. episodes of monitor MAP < 65
    eps = []
    with np.errstate(invalid='ignore'):
        es, ee = runs(np.isfinite(m) & (m < 65))
    for a, b in zip(es, ee):
        L = lab[a:b]
        flagged = np.isin(L, ARTEFACT).mean() >= 0.5
        x = m[a:b]
        e = dict(caseid=cid, dur_s=2 * (b - a), nadir=float(np.nanmin(x)), flagged=bool(flagged),
                 pleth_ok=float(np.mean(np.isfinite(ph[a:b]) & (ph[a:b] >= 40) & (ph[a:b] <= 150))),
                 ecg_ok=float(np.mean((hr[a:b] >= 40) & (hr[a:b] <= 150))))
        for t in ELAPSED:
            k = t // 2
            e[f'nadir_at_{t}'] = float(np.nanmin(x[:k])) if b - a >= k else np.nan
        eps.append(e)
    return out, cuff, eps


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    files = sorted(os.path.join(ROOT, 'data', 'cases', f) for f in os.listdir(os.path.join(ROOT, 'data', 'cases'))
                   if f.endswith('.npz'))
    with Pool(int(os.environ.get('NPROC', 8))) as p:
        res = [r for r in p.imap_unordered(one, files, chunksize=8) if r is not None]
    # restrict to the descriptive cohort
    sys.argv = [sys.argv[0], 'real']
    from analysis import descriptive_cohort   # noqa: E402
    dc = descriptive_cohort()
    keep = set(dc.index)
    res = [r for r in res if r[0]['caseid'] in keep]
    S = {}

    delay = np.array([r[0]['start_delay_min'] for r in res])
    S['start_delay_min'] = dict(median=float(np.median(delay)), q1=float(np.percentile(delay, 25)),
                                q3=float(np.percentile(delay, 75)), share_gt10=float((delay > 10).mean()))

    cuff = pd.DataFrame([c for r in res for c in r[1]])
    base = pd.DataFrame([r[0]['else'] for r in res]).mean()
    cuff = cuff.join(dc[['position']], on='caseid')
    art_cols = ['f_zero', 'f_high', 'f_nonpulsatile', 'f_noise']
    cuff['art'] = cuff[art_cols].sum(1)
    S['cuff_subtype_pre'] = cuff[art_cols + ['f_guard']].mean().to_dict()
    S['cuff_subtype_base'] = base[['zero', 'high', 'nonpulsatile', 'noise', 'guard']].to_dict()
    S['cuff_regular'] = cuff.groupby('regular').agg(n=('art', 'size'), art=('art', 'mean'),
                                                     nonpuls=('f_nonpulsatile', 'mean')).to_dict('index')
    S['cuff_position'] = cuff.groupby('position').agg(n=('art', 'size'), art=('art', 'mean')).query('n >= 200').to_dict('index')
    cuff.to_csv(os.path.join(OUT, 'cuff_readings.csv'), index=False)

    ep = pd.DataFrame([e for r in res for e in r[2]])
    ep.to_csv(os.path.join(OUT, 'episodes_realtime.csv'), index=False)
    bins = [-np.inf, 20, 40, 55, 65]
    names = ['<20', '20-39', '40-54', '55-64']
    rt = []
    for t in ELAPSED:
        g = ep[ep[f'nadir_at_{t}'].notna()].copy()
        g['bin'] = pd.cut(g[f'nadir_at_{t}'], bins, labels=names, right=False)
        for bname, h in g.groupby('bin', observed=True):
            rt.append(dict(elapsed_s=t, nadir_so_far=bname, episodes=len(h), p_flagged=float(h.flagged.mean())))
    pd.DataFrame(rt).to_csv(os.path.join(OUT, 'realtime_table.csv'), index=False)
    deep = ep[ep.nadir < 40]
    S['deep_pulse'] = deep.groupby('flagged').agg(n=('pleth_ok', 'size'), pleth_ok=('pleth_ok', 'mean'),
                                                  ecg_ok=('ecg_ok', 'mean'),
                                                  pleth_ok_ge80=('pleth_ok', lambda v: float((v >= 0.8).mean()))
                                                  ).to_dict('index')
    with open(os.path.join(OUT, 'summary.json'), 'w') as fh:
        json.dump(S, fh, indent=1, default=float)
    print(json.dumps(S, indent=1, default=float))
    print(pd.DataFrame(rt).pivot(index='nadir_so_far', columns='elapsed_s', values='p_flagged').round(2))
