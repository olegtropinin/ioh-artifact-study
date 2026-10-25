"""Per-case extraction: 2-s window features of the 500 Hz arterial waveform,
aligned with the monitor's 2-s numerics. The raw waveform is not kept.

Output: data/cases/<caseid>.npz with float32 arrays on a 2-s grid starting at
the recording start (VitalDB time 0).
"""
import os
import sys
import time
import numpy as np
import vitaldb
from multiprocessing import Pool

FS = 500
WIN = 2 * FS                      # 2-s window, matches the monitor numerics grid
NUM = ['Solar8000/ART_MBP', 'Solar8000/ART_SBP', 'Solar8000/ART_DBP',
       'Solar8000/NIBP_MBP', 'Solar8000/NIBP_SBP', 'Solar8000/NIBP_DBP',
       'Solar8000/HR', 'Solar8000/PLETH_HR', 'Solar8000/PLETH_SPO2']
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'cases')


def window_features(w):
    """Features of each 2-s window, plus pulsatility from a centred 6-s window."""
    n = len(w) // WIN
    x = w[:n * WIN].reshape(n, WIN)
    finite = np.isfinite(x).mean(1)
    with np.errstate(all='ignore'):
        mean = np.nanmean(x, 1)
        mx = np.nanmax(x, 1)
        mn = np.nanmin(x, 1)
        p98 = np.nanpercentile(x, 98, axis=1)
        p02 = np.nanpercentile(x, 2, axis=1)
        d = np.diff(x, axis=1)
        noise = np.nanmedian(np.abs(np.diff(d, axis=1)), 1)   # median |2nd difference|
        maxslope = np.nanmax(np.abs(d), 1) * FS / 10.0         # mmHg per 100 ms
    # pulsatility: max normalised autocorrelation at lags 0.3-2.0 s (HR 30-200)
    puls = np.full(n, np.nan, np.float32)
    hr = np.full(n, np.nan, np.float32)
    lo, hi = int(0.3 * FS), int(2.0 * FS)
    seg = 3 * WIN
    pad = np.concatenate([np.full(WIN, np.nan), w[:n * WIN], np.full(WIN, np.nan)])
    for i in range(n):
        s = pad[i * WIN:i * WIN + seg]
        if np.isfinite(s).mean() < 0.9:
            continue
        s = np.where(np.isfinite(s), s, np.nanmean(s))
        s = s - s.mean()
        if (s * s).sum() <= 1e-6 * seg:          # flat line
            puls[i] = 0.0
            continue
        f = np.fft.rfft(s, 2 * seg)
        ac = np.fft.irfft(f * np.conj(f))[:hi + 1]
        ac = ac / ac[0]
        k = lo + int(np.argmax(ac[lo:hi + 1]))
        puls[i] = ac[k]
        hr[i] = 60.0 * FS / k
    with np.errstate(all='ignore'):
        p90 = np.nanpercentile(x, 90, axis=1)
        p10 = np.nanpercentile(x, 10, axis=1)
    up2, up6 = upstrokes(w, n)
    return dict(w_finite=finite, w_mean=mean, w_max=mx, w_min=mn, w_p98=p98,
                w_p02=p02, w_noise=noise, w_maxslope=maxslope,
                w_puls=puls, w_hr=hr, w_p90=p90, w_p10=p10, w_up2=up2, w_up6=up6)


def upstrokes(w, n, rise=8.0):
    """Systolic upstrokes: peaks of the 100-ms pressure rise > `rise` mmHg, >= 250 ms apart.
    Counted per 2-s window and in the centred 6-s window. Rhythm-independent, so an
    irregular rhythm (e.g. atrial fibrillation) still counts as pulsatile."""
    from scipy.signal import find_peaks
    x = np.where(np.isfinite(w[:n * WIN]), w[:n * WIN], 0.0)
    k = int(0.02 * FS)
    xs = np.convolve(x, np.ones(k) / k, 'same')            # 20-ms smoothing
    lag = int(0.1 * FS)
    r = np.zeros_like(xs)
    r[:-lag] = xs[lag:] - xs[:-lag]
    pk, _ = find_peaks(r, height=rise, distance=int(0.25 * FS))
    c2 = np.bincount(pk // WIN, minlength=n)[:n].astype(np.float32)
    c6 = c2.copy()
    c6[1:] += c2[:-1]
    c6[:-1] += c2[1:]
    return c2, c6


def process(caseid):
    out = os.path.join(OUT, f'{caseid}.npz')
    if os.path.exists(out):
        return caseid, 'cached'
    for attempt in range(4):
        try:
            vf = vitaldb.VitalFile(int(caseid), ['SNUADC/ART'] + NUM)
            break
        except Exception as e:          # network hiccup: retry with backoff
            if attempt == 3:
                return caseid, f'error {e!r}'
            time.sleep(5 * (attempt + 1))
    if 'SNUADC/ART' not in vf.get_track_names():
        return caseid, 'no ART'
    w = vf.to_numpy(['SNUADC/ART'], 1 / FS)[:, 0].astype(np.float32)
    feats = window_features(w)
    n = len(feats['w_mean'])
    num = vf.to_numpy(NUM, 2)
    num = num[:n] if len(num) >= n else np.vstack([num, np.full((n - len(num), len(NUM)), np.nan)])
    arrs = {k: np.asarray(v, np.float32) for k, v in feats.items()}
    for j, name in enumerate(NUM):
        arrs['n_' + name.split('/')[1]] = num[:, j].astype(np.float32)
    np.savez_compressed(out + '.tmp.npz', **arrs)
    os.replace(out + '.tmp.npz', out)
    return caseid, f'ok {n}'


if __name__ == '__main__':
    import pandas as pd
    os.makedirs(OUT, exist_ok=True)
    t = pd.read_csv(os.path.join(OUT, '..', 'trks.csv.gz'))
    ids = sorted(t[t.tname == 'SNUADC/ART'].caseid.unique())
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        ids = ids[:int(sys.argv[2])]
    nproc = int(os.environ.get('NPROC', 10))
    t0 = time.time()
    with Pool(nproc) as p:
        for i, (cid, msg) in enumerate(p.imap_unordered(process, ids), 1):
            print(f'{i}/{len(ids)} {cid} {msg} {time.time() - t0:.0f}s', flush=True)
