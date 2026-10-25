"""V1 injection-recovery: inject synthetic artefacts (after Li, Mark & Clifford 2009)
into clean waveform segments and measure how often the window classifier flags them."""
import glob
import os
import sys
import numpy as np
import pandas as pd
import vitaldb
from scipy.signal import butter, filtfilt
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract import window_features, FS, WIN
from artifact import classify, runs

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SEG = 120 * FS                 # 2-min clean segment
INJ0, INJ1 = 50 * FS, 70 * FS  # injected stretch, 20 s in the middle


def inject(x, kind, rng):
    y = x.copy()
    s = slice(INJ0, INJ1)
    n = INJ1 - INJ0
    t = np.arange(n) / FS
    if kind == 'flush':          # fast flush: square wave to 300 mmHg for 4 s, then ringing
        y[INJ0:INJ0 + 4 * FS] = 300 + rng.normal(0, 1, 4 * FS)
        k = np.arange(2 * FS) / FS
        y[INJ0 + 4 * FS:INJ0 + 6 * FS] += 40 * np.exp(-k * 3) * np.sin(2 * np.pi * 15 * k)
    elif kind == 'zero':         # transducer open to air for 10 s
        y[INJ0:INJ0 + 10 * FS] = rng.normal(0, 0.5, 10 * FS)
    elif kind == 'sample_flat':  # stopcock turned: flat at the current mean for 15 s, then flush 3 s
        y[INJ0:INJ0 + 15 * FS] = x[s].mean() + rng.normal(0, 0.5, 15 * FS)
        y[INJ0 + 15 * FS:INJ0 + 18 * FS] = 300
    elif kind == 'sample_low':   # aspiration: flat at 20 mmHg for 15 s, then flush 3 s
        y[INJ0:INJ0 + 15 * FS] = 20 + rng.normal(0, 0.5, 15 * FS)
        y[INJ0 + 15 * FS:INJ0 + 18 * FS] = 300
    elif kind == 'damping':      # overdamped line: low-pass 1.5 Hz for 20 s (mean preserved)
        b, a = butter(2, 1.5 / (FS / 2))
        y[s] = filtfilt(b, a, x[s])
    elif kind == 'noise':        # motion / electrical noise for 10 s
        y[INJ0:INJ0 + 10 * FS] += rng.normal(0, 25, 10 * FS)
    elif kind == 'offset':       # transducer 20 cm too low: +15 mmHg for 20 s
        y[s] += 15
    return y


KINDS = ['none', 'flush', 'zero', 'sample_flat', 'sample_low', 'damping', 'noise', 'offset']


def one_case(cid):
    rng = np.random.default_rng(cid)
    d = dict(np.load(os.path.join(ROOT, 'data', 'cases', f'{cid}.npz')))
    lab = classify(d)
    s, e = runs(lab == 0)
    ok = (e - s) >= SEG // WIN + 10
    if not ok.any():
        return []
    vf = vitaldb.VitalFile(int(cid), ['SNUADC/ART'])
    w = vf.to_numpy(['SNUADC/ART'], 1 / FS)[:, 0].astype(np.float64)
    out = []
    starts = [(s[i] + 5) * WIN for i in np.flatnonzero(ok)]
    for st in rng.choice(starts, size=min(3, len(starts)), replace=False):
        x = w[st:st + SEG]
        if not np.isfinite(x).all():
            continue
        for kind in KINDS:
            y = inject(x, kind, rng)
            f = window_features(y)
            lb = classify(f)
            inj = slice(INJ0 // WIN, INJ1 // WIN)
            out.append(dict(caseid=cid, start=int(st), kind=kind,
                            frac_flagged=float((lb[inj] != 0).mean()),
                            any_flagged=bool((lb[inj] != 0).any()),
                            outside_flagged=float((np.r_[lb[1:INJ0 // WIN - 6], lb[INJ1 // WIN + 6:-1]] != 0).mean())))
    return out


if __name__ == '__main__':
    files = sorted(glob.glob(os.path.join(ROOT, 'data', 'cases', '*.npz')))
    ids = [int(os.path.basename(f)[:-4]) for f in files]
    rng = np.random.default_rng(20261026)
    pick = sorted(rng.choice(ids, size=min(100, len(ids)), replace=False))
    with Pool(8) as p:
        res = [r for rr in p.map(one_case, pick) for r in rr]
    df = pd.DataFrame(res)
    df.to_csv(os.path.join(ROOT, 'out', 'v1_injection.csv'), index=False)
    print(df.groupby('kind')[['any_flagged', 'frac_flagged', 'outside_flagged']].mean().round(3))
    print('segments', df[df.kind == 'none'].shape[0], 'cases', df.caseid.nunique())
