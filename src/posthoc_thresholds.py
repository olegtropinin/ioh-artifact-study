"""POST HOC (round-1 review): calibrated RORs where the reference association is non-null
(binary exposure below 55 and 60 mmHg), and the measurement-level share of the area below
55 mmHg that artefact contributes without a filter.

python src/posthoc_thresholds.py   -> out/posthoc_review/thresholds.json
"""
import json
import os
import sys

import numpy as np

sys.argv = [sys.argv[0], 'real']
sys.path.insert(0, os.path.dirname(__file__))
import analysis as A                                   # noqa: E402
from models import cohort, load_outcome                # noqa: E402
from posthoc_stats import ror_ci                       # noqa: E402

if __name__ == '__main__':
    c, _ = cohort()
    y = load_outcome(c, 'real')
    S = {}
    for thr in (55, 60):
        er = A.expo(c, 'ref', 'bridged', 'R3', 0, thr, 'binary')
        for f in ('F0', 'F1', 'F3'):
            S[f'binary{thr}_{f}xR3'] = ror_ci(c, y, A.expo(c, 'pipe', f, 'R3', 0, thr, 'binary'), er, seed=thr)
    dc = A.descriptive_cohort()
    for thr in (55, 65):
        ref = A.raw('ref', 'bridged', 'R3', 0, thr, 'auc').reindex(dc.index).to_numpy(float)
        for f in ('F0', 'F1', 'F3'):
            p = A.raw('pipe', f, 'R3', 0, thr, 'auc').reindex(dc.index).to_numpy(float)
            S[f'auc{thr}_{f}xR3_total_ratio'] = float(np.nansum(p) / np.nansum(ref))
            S[f'auc{thr}_{f}xR3_excess_share'] = float(1 - np.nansum(ref) / np.nansum(p))
            S[f'auc{thr}_{f}xR3_top1pct_share_of_excess'] = float(
                np.sort(np.nan_to_num(p - ref))[::-1][:max(1, len(p) // 100)].sum() / np.nansum(np.nan_to_num(p - ref)))
    os.makedirs(os.path.join(A.ROOT, 'out', 'posthoc_review'), exist_ok=True)
    with open(os.path.join(A.ROOT, 'out', 'posthoc_review', 'thresholds.json'), 'w') as fh:
        json.dump(S, fh, indent=1)
    print(json.dumps(S, indent=1))
