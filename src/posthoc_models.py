"""POST HOC (round-1 review): why the canonical exposure is null here, and selection into the
AKI set. Not in the frozen protocol.

python src/posthoc_models.py real   -> out/posthoc_review/models.json
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
import analysis as A                                                   # noqa: E402
from models import cohort, covariates, firth_logit, load_outcome, rcs   # noqa: E402

OUT = os.path.join(A.ROOT, 'out', 'posthoc_review')


def or_ci(X, y):
    b, cov, ok = firth_logit(X, y)
    se = np.sqrt(cov[1, 1])
    return dict(or_=float(np.exp(b[1])), lo=float(np.exp(b[1] - 1.96 * se)), hi=float(np.exp(b[1] + 1.96 * se)))


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    c, _ = cohort()
    y = load_outcome(c, 'real')
    one = np.ones(len(c))
    S = {'events': int(y.sum()), 'n': len(c), 'epv_full': None}
    Zf = covariates(c)
    Zr = covariates(c, reduced=True)
    S['epv_full'] = float(y.sum() / (Zf.shape[1] + 1))
    for label, src, filt in [('reference', 'ref', 'bridged'), ('F1xR3', 'pipe', 'F1')]:
        res = {}
        for metric, thr in [('binary', 65), ('binary', 55), ('minutes', 65)]:
            e = A.expo(c, src, filt, 'R3', 0, thr, metric)
            nodur = Zf[:, [i for i in range(Zf.shape[1])]]  # full set
            res[f'{metric}{thr}'] = {
                'crude': or_ci(np.column_stack([one, e]), y),
                'reduced_set': or_ci(np.column_stack([one, e, Zr]), y),
                'full_set': or_ci(np.column_stack([one, e, Zf]), y),
            }
        S[label] = res
    # without log duration: rebuild the full set minus the duration column
    c2 = c.copy()
    c2['log_dur'] = c2.log_dur.median()      # covariates() uses log_dur; a constant column is dropped below
    Znd = covariates(c2)
    Znd = Znd[:, np.ptp(Znd, 0) > 0]
    e = A.expo(c, 'ref', 'bridged', 'R3', 0, 65, 'binary')
    S['reference']['binary65']['full_set_without_duration'] = or_ci(np.column_stack([one, e, Znd]), y)
    # selection into the AKI set by department (adults, GA, >= 30 min, first case, not transplant)
    dc = A.descriptive_cohort()
    dc = dc[dc.optype != 'Transplantation']
    dc['in_aki_set'] = dc.index.isin(c.index)
    S['aki_set_by_department'] = dc.groupby('department').in_aki_set.agg(['size', 'mean']).to_dict('index')
    S['excluded_no_postop_cr'] = int((dc.cr_base.notna() & dc.cr_max7d.isna()).sum())
    # O6 rule false positives by nadir
    e = pd.read_pickle(os.path.join(A.ROOT, 'out', 'descriptive', 'episodes_labelled.pkl'))
    e['pre_drop'] = e.pre30_max - e.nadir
    e['rule'] = e.pre_drop > 20
    e['flag'] = e.cls == 'flagged'
    out = {}
    for name, g in [('all', e), ('nadir_lt55', e[e.nadir < 55]), ('nadir_lt40', e[e.nadir < 40])]:
        tp = (g.rule & g.flag).sum(); fp = (g.rule & ~g.flag).sum()
        fn = (~g.rule & g.flag).sum(); tn = (~g.rule & ~g.flag).sum()
        out[name] = dict(n=len(g), sens=float(tp / (tp + fn)), spec=float(tn / (tn + fp)), ppv=float(tp / (tp + fp)))
    fpn = e[e.rule & ~e.flag].nadir
    out['fp_nadir_quartiles'] = list(map(float, np.percentile(fpn, [25, 50, 75])))
    out['fp_share_nadir_lt40'] = float((fpn < 40).mean())
    S['o6_rule_by_nadir'] = out
    with open(os.path.join(OUT, 'models.json'), 'w') as fh:
        json.dump(S, fh, indent=1, default=float)
    print(json.dumps(S, indent=1, default=float))
