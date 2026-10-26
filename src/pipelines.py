"""Per-case exposure computation: retrospective-style pipelines on monitor numerics,
and the waveform-referenced series, as specified in docs/protocol.md (incl. amendments).

Grids: R1 = 2-s samples (weight 1/30 min each); R2/R3 = 1-min; R4/R5 = 5/15-min charting
held over each minute of the block (weight 1 min). NaN = no usable value.
"""
import numpy as np
from artifact import classify, runs, ARTEFACT

MIN = 30                         # 2-s samples per minute
THRESHOLDS = (55, 60, 65)
FILTERS = ['F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6']
RES = {'R1': [0], 'R2': [0], 'R3': [0], 'R4': [0, 1, 2, 3, 4], 'R5': [0, 3, 6, 9, 12]}
BRIDGE_MAX = 90                  # windows (3 min)
BRIDGE_SIDE = 15                 # windows (30 s) of valid data needed on each side
DISCORD_MMHG = 10       # monitor vs waveform-mean disagreement flagged in valid windows


# ---------------------------------------------------------------- alignment, period

def best_lag(d, lab, lags=range(1, 5)):
    """Monitor lag behind the waveform (2-s samples), by correlation on valid windows."""
    wm = np.where(lab == 0, d['w_mean'], np.nan)
    num = d['n_ART_MBP']
    best, arg = -2.0, 3
    for lag in lags:
        a, b = wm[:len(wm) - lag], num[lag:]
        k = np.isfinite(a) & np.isfinite(b)
        if k.sum() < 300:
            continue
        r = np.corrcoef(a[k], b[k])[0, 1]
        if r > best:
            best, arg = r, lag
    return arg


def shift(x, lag):
    return np.concatenate([x[lag:], np.full(lag, np.nan, np.float32)])


def first_last_run(mask, a0, a1, min_run=30):
    s, e = runs(mask[a0:a1])
    keep = (e - s) >= min_run
    if not keep.any():
        return None
    p0, p1 = a0 + s[keep][0], a0 + e[keep][-1]
    p1 = p0 + (p1 - p0) // MIN * MIN
    return (p0, p1) if p1 > p0 else None


# ---------------------------------------------------------------- filters (2-s level)

def filter_2s(code, m, s, dd):
    x = m.copy()
    with np.errstate(invalid='ignore'):
        if code == 'F1':
            bad = (m < 20) | (m > 250)
        elif code == 'F2':
            bad = (m < 30) | (m > 200)
        elif code == 'F3':
            bad = (s > 250) | (dd < 15) | (m < 35) | (m > 150) | ((s - dd) < 15)
        elif code in ('F4', 'F5', 'F6'):
            bad = ((m < 20) | (m > 200) | (s > 300) | (s < 20) | (s <= dd)
                   | ((s - dd) < 5) | (dd < 5))
        else:
            bad = np.zeros(len(m), bool)
    x[bad] = np.nan
    return x


def neighbour(v, jump=30):
    """Drop values differing from both grid neighbours by > jump mmHg (Du-style)."""
    x = v.copy()
    prev = np.concatenate([[np.nan], v[:-1]])
    nxt = np.concatenate([v[1:], [np.nan]])
    with np.errstate(invalid='ignore'):
        spike = (np.abs(v - prev) > jump) & (np.abs(v - nxt) > jump)
    x[spike] = np.nan
    return x


def runmed(v, k=7):
    """Centred running median over k grid points, ignoring NaN; NaN stays NaN."""
    h = k // 2
    pad = np.concatenate([np.full(h, np.nan), v, np.full(h, np.nan)])
    win = np.lib.stride_tricks.sliding_window_view(pad, k)
    with np.errstate(all='ignore'):
        out = np.nanmedian(win, 1)
    out[~np.isfinite(v)] = np.nan
    return out


def post_filter(code, v):
    if code == 'F5':
        return neighbour(v)
    if code == 'F6':
        return runmed(v, 7)
    return v


# ---------------------------------------------------------------- sampling

def first_valid(block):
    """First non-NaN value of each row (NaN if none)."""
    ok = np.isfinite(block)
    idx = ok.argmax(1)
    out = block[np.arange(len(block)), idx]
    out[~ok.any(1)] = np.nan
    return out


def chart(x2s, step_min, offset):
    """Charting every step_min minutes from phase offset; the first non-NaN 2-s value in
    each interval is charted. Returns (native chart values, minute -> chart index)."""
    n = len(x2s) // MIN
    bounds = sorted(set([0] + list(range(offset, n, step_min)) + [n]))
    vals, idx = [], np.zeros(n, int)
    for j, (a, b) in enumerate(zip(bounds[:-1], bounds[1:])):
        seg = x2s[a * MIN:b * MIN]
        k = np.flatnonzero(np.isfinite(seg))
        vals.append(seg[k[0]] if len(k) else np.nan)
        idx[a:b] = j
    vals = np.asarray(vals, np.float32)
    return vals, idx


def sample(x2s, res, offset=0, code='F0', sup_min=None):
    """Apply resolution (and post-sampling filter F5/F6 on the native grid).
    Returns (values, weights_in_minutes) on the evaluation grid. Minutes outside the
    common support (sup_min False) are NaN on every grid, so held charts do not cover them."""
    n = len(x2s) // MIN
    if res == 'R1':
        v = post_filter(code, x2s[:n * MIN])
        return v, np.full(len(v), 1 / MIN)
    blk = x2s[:n * MIN].reshape(n, MIN)
    if res == 'R2':
        v = post_filter(code, first_valid(blk))
    elif res == 'R3':
        with np.errstate(all='ignore'):
            v = post_filter(code, np.nanmedian(blk, 1))
    else:
        vals, idx = chart(x2s, 5 if res == 'R4' else 15, offset)
        v = post_filter(code, vals)[idx]
    v = v.astype(np.float32)
    if sup_min is not None:
        v[~sup_min] = np.nan
    return v, np.ones(n)


def exposure(v, w, thr):
    ok = np.isfinite(v)
    below = ok & (v < thr)
    mins = float(w[below].sum())
    auc = float((w * np.where(below, thr - v, 0.0)).sum())
    mon = float(w[ok].sum())
    return mins, auc, (auc / mon if mon else np.nan), mon


# ---------------------------------------------------------------- reference

def bridge(r, lab):
    """Linear bridging of short non-valid gaps bounded by >= 30 s of valid data.
    Returns (bridged series, bridged-flag)."""
    out, flag = r.copy(), np.zeros(len(r), bool)
    s, e = runs(lab != 0)
    for a, b in zip(s, e):
        if b - a > BRIDGE_MAX or a < BRIDGE_SIDE or b + BRIDGE_SIDE > len(r):
            continue
        if (lab[a - BRIDGE_SIDE:a] != 0).any() or (lab[b:b + BRIDGE_SIDE] != 0).any():
            continue
        with np.errstate(all='ignore'):
            v0 = np.nanmedian(r[a - BRIDGE_SIDE:a])
            v1 = np.nanmedian(r[b:b + BRIDGE_SIDE])
        if not (np.isfinite(v0) and np.isfinite(v1)):
            continue
        out[a:b] = np.linspace(v0, v1, b - a + 2)[1:-1]
        flag[a:b] = True
    return out, flag


def reference_2s(m, lab, support, do_bridge=True):
    r = np.where((lab == 0) & support, m, np.nan).astype(np.float32)
    if do_bridge:
        r, fl = bridge(r, lab)
        r[~support] = np.nan
        fl &= support
    else:
        fl = np.zeros(len(r), bool)
    return r, fl


def sample_ref(r, res, offset=0, min_valid=0.5, sup_min=None):
    n = len(r) // MIN
    if res == 'R3':
        blk = r[:n * MIN].reshape(n, MIN)
        ok = np.isfinite(blk).mean(1) >= min_valid
        with np.errstate(all='ignore'):
            v = np.where(ok, np.nanmedian(blk, 1), np.nan)
        return v.astype(np.float32), np.ones(n)
    return sample(r, res, offset, 'F0', sup_min)


# ---------------------------------------------------------------- per case

def run_case(d, anestart, aneend):
    lab0 = classify(d)
    lag = best_lag(d, lab0)
    m = shift(d['n_ART_MBP'], lag)
    s = shift(d['n_ART_SBP'], lag)
    dd = shift(d['n_ART_DBP'], lag)
    # cuff values are not delayed like the arterial numerics: no lag shift (post-unblinding fix, review G-M2)
    nibp = d['n_NIBP_MBP']
    a0 = int(max(0, anestart) // 2)
    a1 = int(min(len(lab0), aneend // 2))
    per = first_last_run(lab0 == 0, a0, a1)
    if per is None:
        return None
    p0, p1 = per
    sl = slice(p0, p1)
    lab = lab0[sl]
    n = (p1 - p0) // MIN
    miss_min = (lab[:n * MIN].reshape(n, MIN) == 1).mean(1) > 0.5
    support = ~np.repeat(miss_min, MIN)
    mm, ss, ddd = m[sl], s[sl], dd[sl]
    rows = []

    # pipelines (primary period)
    def pipes(mmx, ssx, ddx, sup, tag):
        nm = len(sup) // MIN
        supm = sup[:nm * MIN].reshape(nm, MIN).any(1)
        for code in FILTERS:
            x = filter_2s(code, mmx, ssx, ddx)
            x = np.where(sup, x, np.nan)
            for res, offs in RES.items():
                for off in offs:
                    v, w = sample(x, res, off, code, supm)
                    for thr in THRESHOLDS:
                        rows.append((tag, code, res, off, thr) + exposure(v, w, thr))
    pipes(mm, ss, ddd, support, 'pipe')

    # S10: numerics-defined period (monitor MAP 40-150 runs), no waveform information
    with np.errstate(invalid='ignore'):
        nper = first_last_run((m >= 40) & (m <= 150), a0, a1)
    if nper is not None:
        q0, q1 = nper
        pipes(m[q0:q1], s[q0:q1], dd[q0:q1], np.ones(q1 - q0, bool), 'pipe_numper')

    # reference: primary (bridged) at every resolution/offset
    r, rfl = reference_2s(mm, lab, support, True)
    for res, offs in RES.items():
        for off in offs:
            v, w = sample_ref(r, res, off, sup_min=~miss_min)
            for thr in THRESHOLDS:
                rows.append(('ref', 'bridged', res, off, thr) + exposure(v, w, thr))

    # reference sensitivity variants at R3 (and R1 for unbridged)
    variants = {}
    variants['unbridged'] = reference_2s(mm, lab, support, False)[0]
    for name, kw in [('guard0', dict(guard_before_s=0, guard_after_s=0)),
                     ('guard30', dict(guard_before_s=6, guard_after_s=30)),
                     ('pp5', dict(pp_min=5.0)), ('pp12', dict(pp_min=12.0))]:
        lb = classify(d, **kw)[sl]
        variants[name] = reference_2s(mm, lb, support, True)[0]
    wm = d['w_mean'][sl]
    variants['wavemean'] = reference_2s(wm, lab, support, True)[0]
    for name, rv in variants.items():
        v, w = sample_ref(rv, 'R3')
        for thr in THRESHOLDS:
            rows.append(('ref', name, 'R3', 0, thr) + exposure(v, w, thr))
    for name, mv in [('valid25', 0.25), ('valid75', 0.75)]:
        v, w = sample_ref(r, 'R3', 0, mv)
        for thr in THRESHOLDS:
            rows.append(('ref', name, 'R3', 0, thr) + exposure(v, w, thr))
    # post-unblinding variants (review G-M3, G-M4): minute validity counted on observed windows
    # only, and a reference that also drops valid windows where monitor MAP and the waveform mean
    # disagree by > 10 mmHg
    for name, mv in [('valid25_obs', 0.25), ('valid75_obs', 0.75)]:
        v, w = sample_ref(variants['unbridged'], 'R3', 0, mv)
        for thr in THRESHOLDS:
            rows.append(('ref', name, 'R3', 0, thr) + exposure(v, w, thr))
    with np.errstate(invalid='ignore'):
        disc = (lab == 0) & (np.abs(mm - wm) > DISCORD_MMHG)
    lab_c = np.where(disc, 7, lab)
    v, w = sample_ref(reference_2s(mm, lab_c, support, True)[0], 'R3')
    for thr in THRESHOLDS:
        rows.append(('ref', 'concord', 'R3', 0, thr) + exposure(v, w, thr))

    # O2 minute categories and O5 typing (T = 65), filters x R1/R2/R3
    o2 = []
    art_type = np.where(np.isin(lab, [2, 3]), 1, np.where(np.isin(lab, [4, 5]), 2,
                        np.where(lab == 6, 3, 0)))
    for res in ('R1', 'R2', 'R3'):
        rv, _ = sample_ref(r, res, sup_min=~miss_min)
        obs = np.where((lab == 0) & support, 1.0, 0.0)
        if res == 'R1':
            obsf, typ = obs, art_type
        else:
            obsf = obs[:n * MIN].reshape(n, MIN).mean(1)
            t = art_type[:n * MIN].reshape(n, MIN)
            # dominant artefact group of the minute (0 if none)
            cnt = np.stack([(t == g).sum(1) for g in (1, 2, 3)], 1)
            typ = np.where(cnt.sum(1) > 0, cnt.argmax(1) + 1, 0)
        for code in FILTERS:
            x = np.where(support, filter_2s(code, mm, ss, ddd), np.nan)
            v, w = sample(x, res, 0, code, ~miss_min)
            with np.errstate(invalid='ignore'):
                low = np.isfinite(v) & (v < 65)
                spur = low & np.isfinite(rv) & (rv >= 65)
                conf = low & np.isfinite(rv) & (rv < 65) & (obsf >= 0.5)
                blow = low & np.isfinite(rv) & (rv < 65) & (obsf < 0.5)
                ind = low & ~np.isfinite(rv)
                masked = np.isfinite(v) & (v >= 65) & np.isfinite(rv) & (rv < 65)
                hyper = np.isfinite(v) & (v > 120) & np.isfinite(rv) & (rv <= 100)
            o2.append(dict(res=res, filter=code, low=w[low].sum(), spurious=w[spur].sum(),
                           confirmed=w[conf].sum(), bridged_low=w[blow].sum(),
                           indeterminate=w[ind].sum(), masked=w[masked].sum(),
                           spur_g1=w[spur & (typ == 1)].sum(), spur_g2=w[spur & (typ == 2)].sum(),
                           spur_g3=w[spur & (typ == 3)].sum(), spur_g0=w[spur & (typ == 0)].sum(),
                           spurious_hyper=w[hyper].sum(), monitored=w[np.isfinite(v)].sum()))

    # O6 episodes: unfiltered aligned 2-s monitor MAP < 65 within the period
    eps = []
    x = np.where(support, mm, np.nan)
    with np.errstate(invalid='ignore'):
        es, ee = runs(np.isfinite(x) & (x < 65))
    nb = nibp[sl]
    nb_ev = np.flatnonzero(np.isfinite(nb) & ~(np.concatenate([[np.nan], nb[:-1]]) == nb))
    for a, b in zip(es, ee):
        L = lab[a:b]
        pre = x[max(0, a - 15):a]
        near = nb_ev[(nb_ev >= a - 90) & (nb_ev < b + 90)]
        near60 = nb_ev[(nb_ev >= a - 30) & (nb_ev < b + 30)]
        eps.append(dict(start=int(a), dur_s=2 * (b - a), nadir=float(np.nanmin(x[a:b])),
                        pre30_max=float(np.nanmax(pre)) if np.isfinite(pre).any() else np.nan,
                        art_frac=float(np.isin(L, ARTEFACT).mean()),
                        guard_frac=float((L == 6).mean()), valid_frac=float((L == 0).mean()),
                        lab_mode=int(np.bincount(L, minlength=7).argmax()),
                        nibp_near=float(nb[near[np.argmin(np.abs(near - a))]]) if len(near) else np.nan,
                        nibp_near60=float(nb[near60[np.argmin(np.abs(near60 - a))]]) if len(near60) else np.nan))

    # descriptive: label fractions, artefact runs, NIBP-cuff (C3), physiology during nonpulsatile (V3ii)
    hr = shift(d['n_HR'], lag)[sl]
    ph = shift(d['n_PLETH_HR'], lag)[sl]
    np_w = lab == 4
    desc = dict(lag=lag, period_min=n, support_min=int((~miss_min).sum()),
                disc_frac=float(disc[lab == 0].mean()) if (lab == 0).any() else np.nan,
                **{f'frac_{k}': float((lab == i).mean()) for i, k in enumerate(
                    ['valid', 'missing', 'zero', 'high', 'nonpulsatile', 'noise', 'guard'])},
                **{f'runs_{k}': int(len(runs(lab == i)[0])) for i, k in [(2, 'zero'), (3, 'high'), (4, 'nonpulsatile'), (5, 'noise')]},
                nonpuls_n=int(np_w.sum()),
                nonpuls_ecg_ok=int((np_w & (hr >= 40) & (hr <= 150)).sum()),
                nonpuls_pleth_ok=int((np_w & np.isfinite(ph) & (ph >= 40) & (ph <= 150)).sum()))
    # C3: artefact fraction in the 60 s before each NIBP reading vs elsewhere
    pre_mask = np.zeros(len(lab), bool)
    for j in nb_ev:
        pre_mask[max(0, j - 30):j] = True
    art = np.isin(lab, ARTEFACT)
    desc.update(nibp_events=int(len(nb_ev)), art_pre_nibp=float(art[pre_mask].mean()) if pre_mask.any() else np.nan,
                art_else=float(art[~pre_mask].mean()), n_pre_nibp=int(pre_mask.sum()))
    return dict(rows=rows, o2=o2, eps=eps, desc=desc, period=(p0, p1))
