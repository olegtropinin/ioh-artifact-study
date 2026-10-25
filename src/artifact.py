"""Reference classification of 2-s arterial-waveform windows.

Each window gets one label. Only 'valid' windows contribute to the reference MAP.
'missing' (waveform not recorded) is not an artefact: those windows are unverifiable
and are excluded from every series, but they do not create guard windows.
'guard' windows surround artefact runs: the monitor numerics average over several
beats, so they stay contaminated for a few seconds after the waveform recovers.

Thresholds were set on descriptive data only (no outcomes), on 500 cases:
- after a zero/high/non-pulsatile run, |monitor MAP - waveform mean| < 5 mmHg is
  reached within 8 s in 95% of runs (99%: 16 s) -> guard 2 s before, 8 s after;
- median |second difference| is quantised by the ADC step (~1 mmHg); clean windows
  have a 99.9th centile of ~1-2 steps -> noise threshold 4 mmHg;
- a beat-lag autocorrelation criterion for pulsatility was tried and dropped: it flagged
  atrial fibrillation, bigeminy and slow heart rates as non-pulsatile (12% of time in
  patients with preoperative AF vs 1% in sinus rhythm). Pulsatility is instead the
  presence of >= 1 systolic upstroke (pressure rise > 8 mmHg in 100 ms) in the centred
  6-s window, which does not depend on rhythm regularity.
"""
import numpy as np

LABELS = ['valid', 'missing', 'zero', 'high', 'nonpulsatile', 'noise', 'guard']
ARTEFACT = [2, 3, 4, 5]          # labels that are artefact proper
GUARD_BEFORE_S = 2
GUARD_AFTER_S = 8
PP_MIN = 8.0                     # mmHg; below this a window is treated as non-pulsatile
IQR_MIN = 3.0                    # mmHg, p90 - p10: a flat line with occasional spikes
NOISE_MIN = 4.0                  # mmHg, median |second difference|


def classify(d, guard_before_s=GUARD_BEFORE_S, guard_after_s=GUARD_AFTER_S,
             pp_min=PP_MIN, iqr_min=IQR_MIN):
    """Return an int8 array of indices into LABELS, one per 2-s window."""
    mean, pp = d['w_mean'], d['w_p98'] - d['w_p02']
    lab = np.zeros(len(mean), np.int8)
    with np.errstate(invalid='ignore'):
        missing = ~(d['w_finite'] >= 0.9) | ~np.isfinite(mean)
        zero = (np.abs(mean) < 15) & (pp < 10)
        high = (d['w_max'] > 250) | (mean > 200)
        noise = (d['w_min'] < -10) | (d['w_noise'] >= NOISE_MIN)
        nonpuls = (pp < pp_min) | ((d['w_p90'] - d['w_p10']) < iqr_min) | ~(d['w_up6'] >= 1)
    # order matters: the most specific explanation wins
    lab[nonpuls] = 4
    lab[noise] = 5
    lab[high] = 3
    lab[zero] = 2
    lab[missing] = 1
    art = np.isin(lab, ARTEFACT)
    b, a = guard_before_s // 2, guard_after_s // 2
    guard = np.zeros(len(lab), bool)
    for k in range(1, a + 1):          # windows after an artefact window
        guard[k:] |= art[:-k]
    for k in range(1, b + 1):          # windows before an artefact window
        guard[:-k] |= art[k:]
    lab[guard & (lab == 0)] = 6
    return lab


def runs(mask):
    """Start/end (exclusive) indices of contiguous True runs."""
    m = np.concatenate([[False], np.asarray(mask, bool), [False]])
    dm = np.diff(m.astype(int))
    return np.flatnonzero(dm == 1), np.flatnonzero(dm == -1)
