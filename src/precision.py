"""A12 precision check before unblinding. AKI is simulated from ASSUMED covariate effects
(not fitted on the real outcome) and the reference exposure with OR_ref = 1.5; the spread
of log ROR (F1xR3 vs ref@R3) over replicates gives the expected CI half-width."""
import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models import cohort, fit_exposure, ROOT
from analysis import expo

REPS = 300


def main():
    c, _ = cohort()
    rng = np.random.default_rng(11)
    ref = expo(c, 'ref', 'bridged', 'R3', 0, 65, 'binary')
    pip = expo(c, 'pipe', 'F1', 'R3', 0, 65, 'binary')
    age = (c.age.to_numpy(float) - 60) / 10
    ckd = (c.egfr.to_numpy(float) < 60).astype(float)
    asa = (c.asa >= 3).to_numpy(float)
    lin = 0.25 * age + 0.6 * ckd + 0.4 * asa + np.log(1.5) * ref
    # intercept giving ~5.6% AKI
    lo, hi = -10.0, 0.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if np.mean(1 / (1 + np.exp(-(mid + lin)))) < 0.056:
            lo = mid
        else:
            hi = mid
    p = 1 / (1 + np.exp(-(mid + lin)))
    lr = []
    for _ in range(REPS):
        y = (rng.random(len(c)) < p).astype(float)
        bp = fit_exposure(pip, c, y)[0]
        br = fit_exposure(ref, c, y)[0]
        lr.append(bp - br)
    lr = np.array(lr)
    res = dict(n=len(c), prev_ref=float(ref.mean()), prev_pipe=float(pip.mean()),
               discordant=int((ref != pip).sum()), sd_log_ror=float(lr.std(ddof=1)),
               half_width=float(1.96 * lr.std(ddof=1)), mean_ror=float(np.exp(lr.mean())),
               attainable=bool(1.96 * lr.std(ddof=1) <= 0.22))
    os.makedirs(os.path.join(ROOT, 'out'), exist_ok=True)
    json.dump(res, open(os.path.join(ROOT, 'out', 'precision.json'), 'w'), indent=1)
    print(res)


if __name__ == '__main__':
    main()
