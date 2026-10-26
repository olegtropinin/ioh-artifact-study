"""POST HOC (not in the frozen protocol): calibrated intervals for the depth-weighted RORs.

The specification curve showed that, without a filter, depth-weighted exposures (AUC, TWA)
below 55 mmHg gave RORs of 0.3-0.6. The protocol pre-specified only point estimates for
these cells; this script adds intervals with the same A15 method (bootstrap SE vs
permutation-null SD) and is reported as post hoc.

python src/posthoc_depth.py   -> out/results_real/posthoc_depth.csv
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
import analysis as A                                     # noqa: E402
from models import cohort, load_outcome                  # noqa: E402

B = int(os.environ.get('B_PH', 1000))
P = int(os.environ.get('P_PH', 200))

if __name__ == '__main__':
    c, _ = cohort()
    y = load_outcome(c, 'real')
    rows = []
    for metric in ('twa', 'auc'):
        for thr in (55, 65):
            specs = [('ref', A.spec_cols(c, 'ref', 'bridged', 'R3', thr, metric))]
            specs += [(f, A.spec_cols(c, 'pipe', f, 'R3', thr, metric)) for f in ('F0', 'F1', 'F3')]
            est, boots, _ = A.bootstrap(c, y, specs, B, 600000 + thr)
            nulls = A.perm_null(c, y, specs, P, 700000 + thr)
            for k, (f, _) in enumerate(specs[1:], 1):
                lo, hi, s = A.calibrated(est[k] - est[0], boots[:, k] - boots[:, 0], nulls[:, k] - nulls[:, 0])
                rows.append(dict(metric=metric, thr=thr, filter=f, res='R3',
                                 or_ref=np.exp(est[0]), or_pipe=np.exp(est[k]),
                                 ror=np.exp(est[k] - est[0]), lo=lo, hi=hi,
                                 p_perm=float(np.mean(np.abs(nulls[:, k] - nulls[:, 0]) >= abs(est[k] - est[0])))))
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(A.ROOT, 'out', 'results_real', 'posthoc_depth.csv'), index=False)
    print(out.round(3).to_string())
