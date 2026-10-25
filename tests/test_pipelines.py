"""Unit tests on synthetic series with known exposure (protocol amendment A2)."""
import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from pipelines import (sample, sample_ref, exposure, filter_2s, bridge, chart, runmed,
                       neighbour, MIN, reference_2s)
from artifact import classify


def series(minutes, value):
    return np.full(minutes * MIN, value, np.float32)


def test_exposure_minutes_auc_twa_r3():
    x = np.concatenate([series(10, 60), series(10, 80)])
    v, w = sample(x, 'R3')
    mins, auc, twa, mon = exposure(v, w, 65)
    assert mins == 10 and auc == 50 and mon == 20 and twa == 2.5


def test_exposure_r1_counts_two_second_samples_as_minutes():
    x = np.concatenate([series(3, 50), series(7, 90)])
    v, w = sample(x, 'R1')
    mins, auc, _, mon = exposure(v, w, 65)
    assert np.isclose(mins, 3) and np.isclose(auc, 45) and np.isclose(mon, 10)


def test_r2_takes_first_non_nan_value_of_minute():
    x = series(2, 80)
    x[0:3] = np.nan
    x[3] = 50
    v, _ = sample(x, 'R2')
    assert v[0] == 50 and v[1] == 80


def test_r5_chart_is_held_and_phase_shifted():
    x = np.concatenate([series(15, 50), series(15, 90)])
    v0, _ = sample(x, 'R5', 0)
    assert (v0[:15] == 50).all() and (v0[15:] == 90).all()
    v3, _ = sample(x, 'R5', 3)
    assert (v3[:3] == 50).all() and (v3[3:18] == 50).all() and (v3[18:] == 90).all()


def test_support_mask_blanks_held_minutes():
    x = series(15, 50)
    sup = np.ones(15, bool)
    sup[5:10] = False
    v, w = sample(x, 'R5', 0, 'F0', sup)
    mins, _, _, mon = exposure(v, w, 65)
    assert mins == 10 and mon == 10


def test_filters_follow_published_rules():
    m = np.array([15, 25, 260, 40, 60], np.float32)
    s = np.array([30, 40, 300, 50, 100], np.float32)
    d = np.array([10, 20, 200, 38, 40], np.float32)
    f1 = filter_2s('F1', m, s, d)
    assert np.isnan(f1[0]) and np.isnan(f1[2]) and f1[1] == 25
    f2 = filter_2s('F2', m, s, d)
    assert np.isnan(f2[1]) and f2[3] == 40
    f3 = filter_2s('F3', m, s, d)   # PP 12 < 15 at index 3 -> dropped; DBP 10 < 15 at 0
    assert np.isnan(f3[0]) and np.isnan(f3[3]) and f3[4] == 60


def test_neighbour_and_running_median():
    v = np.array([80, 80, 20, 80, 80], np.float32)
    assert np.isnan(neighbour(v)[2])
    assert runmed(v, 3)[2] == 80


def test_bridge_interpolates_short_gap_only_with_valid_sides():
    lab = np.zeros(100, np.int8)
    lab[40:60] = 2
    r = np.where(lab == 0, np.where(np.arange(100) < 40, 70.0, 80.0), np.nan).astype(np.float32)
    out, fl = bridge(r, lab)
    assert fl[40:60].all() and not fl[:40].any()
    assert 70 < out[50] < 80
    lab2 = lab.copy()
    lab2[30] = 4                     # less than 30 s of valid data before the gap
    out2, fl2 = bridge(np.where(lab2 == 0, r, np.nan), lab2)
    assert not fl2[40:60].any()


def test_reference_r3_needs_half_valid_minute():
    lab = np.zeros(2 * MIN, np.int8)
    lab[:20] = 4                      # 2/3 of minute 0 non-valid; no bridging (too short sides)
    m = series(2, 60)
    r, _ = reference_2s(m, lab, np.ones(len(m), bool), do_bridge=False)
    v, _ = sample_ref(r, 'R3')
    assert np.isnan(v[0]) and v[1] == 60


def test_classifier_labels_zero_and_guard():
    n = 20
    d = dict(w_finite=np.ones(n), w_mean=np.full(n, 80.0), w_max=np.full(n, 120.0),
             w_min=np.full(n, 60.0), w_p98=np.full(n, 118.0), w_p02=np.full(n, 62.0),
             w_noise=np.full(n, 1.0), w_maxslope=np.full(n, 100.0),
             w_puls=np.full(n, 0.8), w_hr=np.full(n, 70.0), w_p90=np.full(n, 110.0),
             w_p10=np.full(n, 65.0), w_up6=np.full(n, 6.0), w_up2=np.full(n, 2.0))
    for k in ('w_mean', 'w_max', 'w_min', 'w_p98', 'w_p02'):
        d[k][5] = 0.5
    lab = classify(d)
    assert lab[5] == 2
    assert lab[4] == 6 and (lab[6:10] == 6).all() and lab[10] == 0 and lab[3] == 0


def test_missing_does_not_create_guard():
    n = 10
    d = dict(w_finite=np.ones(n), w_mean=np.full(n, 80.0), w_max=np.full(n, 120.0),
             w_min=np.full(n, 60.0), w_p98=np.full(n, 118.0), w_p02=np.full(n, 62.0),
             w_noise=np.full(n, 1.0), w_maxslope=np.full(n, 100.0),
             w_puls=np.full(n, 0.8), w_hr=np.full(n, 70.0), w_p90=np.full(n, 110.0),
             w_p10=np.full(n, 65.0), w_up6=np.full(n, 6.0), w_up2=np.full(n, 2.0))
    d['w_finite'][5] = 0.0
    lab = classify(d)
    assert lab[5] == 1 and lab[6] == 0 and lab[4] == 0


def test_irregular_rhythm_is_not_nonpulsatile():
    n = 10
    d = dict(w_finite=np.ones(n), w_mean=np.full(n, 70.0), w_max=np.full(n, 110.0),
             w_min=np.full(n, 50.0), w_p98=np.full(n, 108.0), w_p02=np.full(n, 52.0),
             w_noise=np.full(n, 1.0), w_maxslope=np.full(n, 100.0),
             w_puls=np.full(n, 0.1), w_hr=np.full(n, 90.0), w_p90=np.full(n, 100.0),
             w_p10=np.full(n, 55.0), w_up6=np.full(n, 8.0), w_up2=np.full(n, 3.0))
    assert (classify(d) == 0).all()          # low autocorrelation alone is not an artefact
    d['w_up6'][4] = 0                         # no upstroke in 6 s -> non-pulsatile
    assert classify(d)[4] == 4
