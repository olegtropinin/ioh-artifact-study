"""POST HOC (round-1 review G-M1): injection-recovery sweep over artefact amplitude and type.

The original V1 injected artefacts sized to cross the classifier's own thresholds. This sweep
varies amplitude and duration, adds artefacts the rules were not designed for (partial
occlusion, slow drift, ringing, sampling without a terminal flush) and reports detection by
artefact labels proper (zero/high/non-pulsatile/noise), excluding guard.

python src/validate_v1_sweep.py   -> out/v1_sweep.csv
"""
import os
import sys
from multiprocessing import Pool

import numpy as np
import pandas as pd
import vitaldb
from scipy.signal import butter, filtfilt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artifact import ARTEFACT, classify, runs          # noqa: E402
from extract import FS, WIN, window_features           # noqa: E402
import validate_v1 as V                                 # noqa: E402

ROOT = V.ROOT
A0, A1 = V.INJ0, V.INJ1


def variants():
    out = [('none', None)]
    out += [('flush', (amp, dur)) for amp in (120, 150, 200, 250, 300) for dur in (0.5, 1, 2, 4)]
    out += [('zero_level', lvl) for lvl in (0, 5, 10, 15, 20, 25)]
    out += [('damping_hz', hz) for hz in (1.5, 2, 3, 5, 10)]
    out += [('partial_occlusion', k) for k in (0.5, 0.3, 0.15)]
    out += [('drift_mmhg', dmm) for dmm in (10, 20, 40)]
    out += [('ringing_mmhg', a) for a in (5, 10, 20)]
    out += [('sampling_no_flush', lvl) for lvl in ('mean', 20)]
    return out


def inject(x, kind, p, rng):
    y = x.copy()
    n = A1 - A0
    t = np.arange(n) / FS
    if kind == 'flush':
        amp, dur = p
        k = int(dur * FS)
        y[A0:A0 + k] = amp + rng.normal(0, 1, k)
    elif kind == 'zero_level':
        y[A0:A0 + 10 * FS] = p + rng.normal(0, 0.5, 10 * FS)
    elif kind == 'damping_hz':
        b, a = butter(2, p / (FS / 2))
        y[A0:A1] = filtfilt(b, a, x[A0:A1])
    elif kind == 'partial_occlusion':
        m = x[A0:A1].mean()
        y[A0:A1] = m - 10 * (1 - p) + p * (x[A0:A1] - m)
    elif kind == 'drift_mmhg':
        y[A0:A1] += p * t / t[-1]
    elif kind == 'ringing_mmhg':
        y[A0:A1] += p * np.sin(2 * np.pi * 18 * t)
    elif kind == 'sampling_no_flush':
        lvl = x[A0:A1].mean() if p == 'mean' else p
        y[A0:A0 + 15 * FS] = lvl + rng.normal(0, 0.5, 15 * FS)
    return y


def one_case(cid):
    rng = np.random.default_rng(cid + 7)
    d = dict(np.load(os.path.join(ROOT, 'data', 'cases', f'{cid}.npz')))
    lab = classify(d)
    s, e = runs(lab == 0)
    ok = (e - s) >= V.SEG // WIN + 10
    if not ok.any():
        return []
    w = vitaldb.VitalFile(int(cid), ['SNUADC/ART']).to_numpy(['SNUADC/ART'], 1 / FS)[:, 0].astype(np.float64)
    out = []
    starts = [(s[i] + 5) * WIN for i in np.flatnonzero(ok)]
    for st in rng.choice(starts, size=min(2, len(starts)), replace=False):
        x = w[st:st + V.SEG]
        if not np.isfinite(x).all():
            continue
        for kind, p in variants():
            lb = classify(window_features(inject(x, kind, p, rng)))
            inj = lb[A0 // WIN:A1 // WIN]
            out.append(dict(caseid=cid, kind=kind, param=str(p),
                            any_artefact=bool(np.isin(inj, ARTEFACT).any()),
                            frac_artefact=float(np.isin(inj, ARTEFACT).mean()),
                            any_incl_guard=bool((inj != 0).any())))
    return out


if __name__ == '__main__':
    import glob
    files = sorted(glob.glob(os.path.join(ROOT, 'data', 'cases', '*.npz')))
    ids = [int(os.path.basename(f)[:-4]) for f in files]
    pick = sorted(np.random.default_rng(20261027).choice(ids, size=60, replace=False))
    with Pool(8) as pool:
        res = [r for rr in pool.map(one_case, pick) for r in rr]
    df = pd.DataFrame(res)
    df.to_csv(os.path.join(ROOT, 'out', 'v1_sweep.csv'), index=False)
    t = df.groupby(['kind', 'param'], sort=False)[['any_artefact', 'frac_artefact', 'any_incl_guard']].mean().round(2)
    print(t.to_string())
    print('segments', (df.kind == 'none').sum(), 'cases', df.caseid.nunique())
