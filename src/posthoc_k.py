"""POST HOC (round-2 review): A15 interval and verdict for the primary ROR if k of the 28
upward-moved patients had developed AKI (outcomes swapped with k concordant cases, so the
event count is unchanged).

python src/posthoc_k.py   -> out/posthoc_review/ror_by_k.json
"""
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

sys.argv = [sys.argv[0], 'real']
sys.path.insert(0, os.path.dirname(__file__))
import analysis as A                                   # noqa: E402
from models import cohort, load_outcome                # noqa: E402
from posthoc_stats import ror_ci                       # noqa: E402


def one(k):
    c, _ = cohort()
    y = load_outcome(c, 'real')
    ep = A.expo(c, 'pipe', 'F1', 'R3', 0, 65, 'binary')
    er = A.expo(c, 'ref', 'bridged', 'R3', 0, 65, 'binary')
    up = np.flatnonzero(ep > er)
    conc = np.flatnonzero((ep == er) & (y == 1))
    rng = np.random.default_rng(100 + k)
    yy = y.copy()
    if k:
        yy[rng.choice(up, k, replace=False)] = 1
        yy[rng.choice(conc, k, replace=False)] = 0
    r = ror_ci(c, yy, ep, er, B=400, P=200, seed=k)
    lo, hi, ror = r['lo'], r['hi'], r['ror']
    verdict = 'equivalent' if lo >= 0.8 and hi <= 1.25 else (
        'material change' if (lo > 1 or hi < 1) and not (0.8 <= ror <= 1.25) else 'inconclusive')
    return dict(k=k, **r, verdict=verdict)


if __name__ == '__main__':
    with Pool(6) as p:
        res = p.map(one, range(6))
    with open(os.path.join(A.ROOT, 'out', 'posthoc_review', 'ror_by_k.json'), 'w') as fh:
        json.dump(res, fh, indent=1)
    for r in res:
        print(r)
