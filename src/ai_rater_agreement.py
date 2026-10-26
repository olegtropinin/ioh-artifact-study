"""Agreement between the blinded AI rater (secondary validation) and the window classifier.

Inputs: out/adjudication/ai_rater_part{1,2}.csv (ratings), key_hidden.csv (classifier label per
snippet; kept out of version control). Prompt and blinding conditions: docs/ai_rater_prompt.md.

python src/ai_rater_agreement.py   -> out/adjudication/ai_rater_agreement.json
"""
import json
import os

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADJ = os.path.join(ROOT, 'out', 'adjudication')

if __name__ == '__main__':
    r = pd.concat([pd.read_csv(os.path.join(ADJ, f'ai_rater_part{i}.csv')) for i in (1, 2)])
    k = pd.read_csv(os.path.join(ADJ, 'key_hidden.csv'))
    m = r.merge(k, on='snippet')
    m['alg'] = np.where(m.label.isin([2, 3, 4, 5]), 'artefact', np.where(m.label == 6, 'guard', 'valid'))
    print(pd.crosstab(m.alg, m.rating, margins=True))
    print(pd.crosstab(m.stratum, m.rating))
    d = m[(m.rating != 'unsure') & (m.alg != 'guard')]
    a, b = d.alg == 'artefact', d.rating == 'artefact'
    po = (a == b).mean()
    pe = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())
    res = dict(n_rated=int(len(m)), n=int(len(d)), agree=float(po), kappa=float((po - pe) / (1 - pe)),
               artefact_share_in_subset=float(a.mean()),
               alg_artefact_rated_artefact=float(b[a].mean()), alg_valid_rated_artefact=float(b[~a].mean()),
               alg_valid_n=int((~a).sum()), alg_valid_low_strata_n=int((~a & d.stratum.str.startswith('B')).sum()),
               guard_n=int((m.alg == 'guard').sum()),
               guard_rated_artefact=float((m[m.alg == 'guard'].rating == 'artefact').mean()),
               unsure=int((m.rating == 'unsure').sum()))
    with open(os.path.join(ADJ, 'ai_rater_agreement.json'), 'w') as fh:
        json.dump(res, fh, indent=1)
    print(res)
