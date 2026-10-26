"""Outcome models (protocol section 6 with amendments A3, A6, A7, A12).

The outcome vector is loaded through load_outcome(mode): 'permuted' (seeded permutation,
used for the pre-freeze dry run and precision checks) or 'real' (only after the freeze tag).
"""
import os
import hashlib
import numpy as np
import pandas as pd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CACHE = os.path.join(ROOT, 'out', 'cache')


# ---------------------------------------------------------------- Firth logistic

def firth_logit(X, y, max_iter=200, tol=1e-7):
    """Firth-penalised logistic regression (Newton-Raphson with step halving).
    Returns (beta, cov, converged)."""
    n, p = X.shape
    beta = np.zeros(p)

    def pen_ll(b):
        eta = X @ b
        pr = 1 / (1 + np.exp(-eta))
        w = pr * (1 - pr)
        info = X.T @ (X * w[:, None])
        sign, logdet = np.linalg.slogdet(info)
        ll = np.sum(y * eta - np.logaddexp(0, eta))
        return ll + 0.5 * logdet, pr, w, info

    ll, pr, w, info = pen_ll(beta)
    for _ in range(max_iter):
        try:
            inv = np.linalg.inv(info)
        except np.linalg.LinAlgError:
            return beta, np.full((p, p), np.nan), False
        xw = X * np.sqrt(w)[:, None]
        h = np.einsum('ij,jk,ik->i', xw, inv, xw)
        score = X.T @ (y - pr + h * (0.5 - pr))
        step = inv @ score
        t = 1.0
        for _ in range(30):
            nb = beta + t * step
            nll, npr, nw, ninfo = pen_ll(nb)
            if np.isfinite(nll) and nll >= ll - 1e-10:
                break
            t /= 2
        beta, ll, pr, w, info = nb, nll, npr, nw, ninfo
        if np.max(np.abs(t * step)) < tol:
            try:
                return beta, np.linalg.inv(info), True
            except np.linalg.LinAlgError:
                return beta, np.full((p, p), np.nan), False
    return beta, np.linalg.pinv(info), False


# ---------------------------------------------------------------- design matrix

def rcs(x, knots):
    """Restricted cubic spline basis (Harrell), 3 knots -> 1 non-linear column."""
    k1, k2, k3 = knots
    pos = lambda u: np.maximum(u, 0) ** 3
    return (pos(x - k1) - pos(x - k2) * (k3 - k1) / (k3 - k2)
            + pos(x - k3) * (k2 - k1) / (k3 - k2)) / (k3 - k1) ** 2


COV_CONT = ['bmi', 'preop_hb', 'preop_alb', 'log_dur']
COV_BIN = ['female', 'asa3', 'emop', 'preop_htn', 'preop_dm']


def covariates(df, reduced=False):
    """Adjustment-set matrix. Imputation uses the medians/modes of df itself, so it is
    recomputed inside every bootstrap resample."""
    cols = []
    for v, kn in [('age', None), ('egfr', None)]:
        x = df[v].astype(float).to_numpy()
        x = np.where(np.isfinite(x), x, np.nanmedian(x))
        knots = np.percentile(x, [10, 50, 90])
        cols += [x / 10, rcs(x, knots) / 10]
    cols += [df.asa3.to_numpy(float), df.emop.to_numpy(float)]
    if reduced:
        return np.column_stack(cols)
    for v in COV_CONT:
        x = df[v].astype(float).to_numpy()
        miss = ~np.isfinite(x)
        x = np.where(miss, np.nanmedian(x), x)
        cols.append(x)
        if miss.mean() > 0.05:
            cols.append(miss.astype(float))
    for v in ['female', 'preop_htn', 'preop_dm']:
        cols.append(df[v].fillna(0).to_numpy(float))
    for v, levels in [('department', ['Thoracic surgery', 'Gynecology', 'Urology']),
                      ('approach', ['Videoscopic', 'Robotic'])]:
        for L in levels:
            cols.append((df[v] == L).to_numpy(float))
    return np.column_stack(cols)


def fit_exposure(expo, df, y, reduced=False):
    """log-OR (and SE) of the exposure column, adjusted."""
    Z = covariates(df, reduced)
    X = np.column_stack([np.ones(len(df)), expo, Z])
    keep = np.ptp(X, 0) > 0
    keep[0] = keep[1] = True
    b, cov, ok = firth_logit(X[:, keep], y)
    return b[1], np.sqrt(cov[1, 1]) if np.isfinite(cov[1, 1]) else np.nan, ok


# ---------------------------------------------------------------- cohort

def cohort(skip=()):
    """Analysis set: one case per subject, eligible for AKI analysis, >= 30 min reference
    monitoring. Returns covariate frame indexed by caseid. `skip` names selection steps to omit
    (used only by post hoc sensitivity analyses)."""
    c = pd.read_pickle(os.path.join(ROOT, 'data', 'cohort_raw.pkl')).set_index('caseid')
    desc = pd.read_pickle(os.path.join(CACHE, 'desc.pkl')).set_index('caseid')
    x = pd.read_pickle(os.path.join(CACHE, 'exposures.pkl'))
    refmon = x[(x.family == 'ref') & (x['filter'] == 'bridged') & (x.res == 'R3')
               & (x.thr == 65)].set_index('caseid').monitored
    c = c.join(desc, how='inner').join(refmon.rename('ref_monitored'), how='inner')
    flow = [('ART waveform, monitoring period found', len(c))]
    steps = [('age >= 18', c.age >= 18),
             ('general anaesthesia', c.ane_type == 'General'),
             ('>= 30 min reference-valid monitoring', c.ref_monitored >= 30),
             ('not transplantation', c.optype != 'Transplantation'),
             ('baseline creatinine available', c.cr_base.notna()),
             ('baseline eGFR >= 15', c.egfr >= 15),
             ('creatinine within 7 days after surgery', c.cr_max7d.notna())]
    for name, m in steps:
        if name in skip:
            continue
        c = c[m.loc[c.index]]
        flow.append((name, len(c)))
    c = c.sort_index()
    c = c[~c.subjectid.duplicated(keep='first')]
    flow.append(('first eligible case per patient', len(c)))
    c['asa3'] = (c.asa >= 3).astype(float)
    c['log_dur'] = np.log(c.ane_dur_h.clip(lower=0.25))
    return c, flow


def load_outcome(c, mode, col='aki', seed=20261026):
    y = c[col].to_numpy(float)
    if mode == 'permuted':
        y = np.random.default_rng(seed).permutation(y)
    elif mode != 'real':
        raise ValueError(mode)
    return y


def code_hash():
    h = hashlib.sha256()
    for f in sorted(os.listdir(os.path.join(ROOT, 'src'))):
        if f.endswith('.py'):
            h.update(open(os.path.join(ROOT, 'src', f), 'rb').read())
    return h.hexdigest()
