"""A1 adjudication set: 400 stratified 40-s waveform snippets, plotted without any label
or numerics, with a hidden key and a blank rating form. Also 6-snippet grids for the
blinded AI rater (V2, secondary)."""
import hashlib
import os
import sys
import numpy as np
import pandas as pd
import vitaldb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models import ROOT, CACHE
from analysis import descriptive_cohort
from artifact import classify, ARTEFACT
from pipelines import best_lag, shift

OUT = os.path.join(ROOT, 'out', 'adjudication')
STRATA = {'A_low_flagged': 100, 'A_low_guard_only': 50, 'B_low_valid': 100,
          'C_random_valid': 100, 'D_flagged_map_ge65': 50}


def h(x):
    return int(hashlib.sha256(str(x).encode()).hexdigest(), 16)


def candidates(c):
    desc = pd.read_pickle(os.path.join(CACHE, 'desc.pkl')).set_index('caseid')
    rows = []
    for cid in c.index:
        d = dict(np.load(os.path.join(ROOT, 'data', 'cases', f'{cid}.npz')))
        lab = classify(d)
        lag = best_lag(d, lab)
        m = shift(d['n_ART_MBP'], lag)
        p0, p1 = desc.loc[cid, ['p0', 'p1']].astype(int)
        i = np.arange(p0 + 10, p1 - 10)
        L, M = lab[i], m[i]
        with np.errstate(invalid='ignore'):
            sets = {'A_low_flagged': i[(M < 65) & np.isin(L, ARTEFACT)],
                    'A_low_guard_only': i[(M < 65) & (L == 6)],
                    'B_low_valid': i[(M < 65) & (L == 0)],
                    'C_random_valid': i[L == 0],
                    'D_flagged_map_ge65': i[(M >= 65) & np.isin(L, ARTEFACT)]}
        r = np.random.default_rng(h(cid) % 2**32)
        for s, idx in sets.items():
            if len(idx):
                rows.append(dict(caseid=cid, subjectid=c.subjectid[cid], stratum=s,
                                 win=int(r.choice(idx)), label=int(lab[r.choice(idx)])))
    return pd.DataFrame(rows)


def main():
    os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)
    c = descriptive_cohort()
    cand = candidates(c)
    cand['key'] = [h(f'{s}-{sub}') for s, sub in zip(cand.stratum, cand.subjectid)]
    picks, used = [], {}
    for s, n in STRATA.items():
        g = cand[cand.stratum == s].sort_values('key')
        k = 0
        for _, row in g.iterrows():
            if used.get(row.subjectid, 0) >= 2:
                continue
            picks.append(row)
            used[row.subjectid] = used.get(row.subjectid, 0) + 1
            k += 1
            if k == n:
                break
    P = pd.DataFrame(picks).reset_index(drop=True)
    P = P.sample(frac=1, random_state=1).reset_index(drop=True)     # shuffle strata
    P['snippet'] = [f'S{i + 1:03d}' for i in range(len(P))]
    # re-read the label of the exact window
    labs = {}
    for cid in P.caseid.unique():
        d = dict(np.load(os.path.join(ROOT, 'data', 'cases', f'{cid}.npz')))
        labs[cid] = classify(d)
    P['label'] = [int(labs[cid][w]) for cid, w in zip(P.caseid, P.win)]
    P.to_csv(os.path.join(OUT, 'key_hidden.csv'), index=False)
    pd.DataFrame(dict(snippet=P.snippet, rating='', artefact_type='', rater='')).to_csv(
        os.path.join(OUT, 'rating_form.csv'), index=False)
    # plot
    waves = {}
    for cid in P.caseid.unique():
        waves[cid] = vitaldb.VitalFile(int(cid), ['SNUADC/ART']).to_numpy(['SNUADC/ART'], 1 / 500)[:, 0]
    for _, r in P.iterrows():
        w = waves[r.caseid]
        a, b = max(0, (r.win - 9) * 1000), (r.win + 11) * 1000
        t = (np.arange(a, b) - r.win * 1000) / 500
        fig, ax = plt.subplots(figsize=(8, 2.2))
        ax.plot(t, w[a:b], lw=0.6, color='k')
        ax.axvspan(0, 2, color='gold', alpha=0.35)
        ax.set_xlabel('s'); ax.set_ylabel('mmHg'); ax.set_title(r.snippet, fontsize=9)
        fig.tight_layout(); fig.savefig(os.path.join(OUT, 'img', f'{r.snippet}.png'), dpi=80); plt.close(fig)
    # AI-rater subset: 150 snippets in grids of 6
    ai = P.groupby('stratum', group_keys=False).apply(lambda g: g.head(int(round(150 * len(g) / len(P)))))
    ai = ai.sort_values('snippet').reset_index(drop=True)
    os.makedirs(os.path.join(OUT, 'grids'), exist_ok=True)
    for gi in range(0, len(ai), 6):
        sub = ai.iloc[gi:gi + 6]
        fig, axs = plt.subplots(len(sub), 1, figsize=(9, 1.9 * len(sub)))
        for ax, (_, r) in zip(np.atleast_1d(axs), sub.iterrows()):
            w = waves[r.caseid]
            a, b = max(0, (r.win - 9) * 1000), (r.win + 11) * 1000
            ax.plot((np.arange(a, b) - r.win * 1000) / 500, w[a:b], lw=0.6, color='k')
            ax.axvspan(0, 2, color='gold', alpha=0.35)
            ax.set_title(r.snippet, fontsize=9, loc='left')
        fig.tight_layout(); fig.savefig(os.path.join(OUT, 'grids', f'grid_{gi // 6 + 1:02d}.png'), dpi=70); plt.close(fig)
    ai[['snippet']].to_csv(os.path.join(OUT, 'ai_subset.csv'), index=False)
    print(P.stratum.value_counts().to_dict(), 'AI subset', len(ai), 'grids', (len(ai) + 5) // 6)


if __name__ == '__main__':
    main()
