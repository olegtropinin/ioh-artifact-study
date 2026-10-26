"""Null calibration of the paired-bootstrap ROR interval (run before unblinding).

Under a randomly permuted outcome both odds ratios are 1 in the population, so the true ROR
is exactly 1. Over many permutations, a well-calibrated 95% interval covers 1 in ~95%.
The real outcome is never used: permutations start from the protocol's permuted vector.

python src/null_calibration.py   -> out/null_calibration.json
"""
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from analysis import expo, offsets                      # noqa: E402
from models import cohort, fit_exposure, load_outcome   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N_PERM = int(os.environ.get('N_PERM', 100))
B = int(os.environ.get('B_CAL', 200))
PAIRS = [('F1', 'R3'), ('F0', 'R1'), ('F3', 'R2'), ('F6', 'R3')]
STATE = {}


def _init():
    c, _ = cohort()
    y0 = load_outcome(c, 'permuted')
    cols = {}
    for f, r in PAIRS:
        cols[(f, r)] = [expo(c, 'pipe', f, r, o, 65, 'binary') for o in offsets(r)]
        cols[('ref', r)] = [expo(c, 'ref', 'bridged', r, o, 65, 'binary') for o in offsets(r)]
    STATE.update(c=c, y0=y0, cols=cols)


def _lor(key, idx, y):
    c = STATE['c']
    return np.mean([fit_exposure(e[idx], c.iloc[idx], y[idx])[0] for e in STATE['cols'][key]])


def _one(p):
    c, y0 = STATE['c'], STATE['y0']
    y = np.random.default_rng(70000 + p).permutation(y0)
    n = len(c)
    full = np.arange(n)
    out = {}
    for f, r in PAIRS:
        hat = _lor((f, r), full, y) - _lor(('ref', r), full, y)
        bs = []
        for b in range(B):
            idx = np.random.default_rng(10 ** 6 * (p + 1) + b).integers(0, n, n)
            bs.append(_lor((f, r), idx, y) - _lor(('ref', r), idx, y))
        lo, hi = np.percentile(bs, [2.5, 97.5])
        out[f'{f}x{r}'] = dict(lror=float(hat), lo=float(lo), hi=float(hi), se=float(np.std(bs, ddof=1)))
    return out


if __name__ == '__main__':
    with Pool(int(os.environ.get('NPROC', 8)), initializer=_init) as pool:
        res = pool.map(_one, range(N_PERM))
    summ = {}
    for f, r in PAIRS:
        k = f'{f}x{r}'
        L = np.array([x[k]['lror'] for x in res])
        lo = np.array([x[k]['lo'] for x in res])
        hi = np.array([x[k]['hi'] for x in res])
        se = np.array([x[k]['se'] for x in res])
        summ[k] = dict(perms=N_PERM, B=B, coverage_of_1=float(np.mean((lo <= 0) & (hi >= 0))),
                       null_sd_lror=float(L.std(ddof=1)), mean_boot_se=float(se.mean()),
                       se_ratio=float(se.mean() / L.std(ddof=1)),
                       null_ror_2_5=float(np.exp(np.percentile(L, 2.5))),
                       null_ror_97_5=float(np.exp(np.percentile(L, 97.5))),
                       inside_margin=float(np.mean((np.exp(lo) >= 0.8) & (np.exp(hi) <= 1.25))))
    with open(os.path.join(ROOT, 'out', 'null_calibration.json'), 'w') as fh:
        json.dump(dict(summary=summ, runs=res), fh, indent=1)
    print(json.dumps(summ, indent=1))
