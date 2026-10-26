"""POST HOC: artefact before cuff readings by arterial cannulation site (radial vs pedal/femoral).

An arm cuff cannot occlude a pedal or femoral catheter, so these patients are a natural
negative control for the cuff-occlusion explanation of the peri-cuff artefact excess.

python src/posthoc_cuff_site.py   -> out/descriptive/c3_by_site.csv
"""
import os

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    d = pd.read_pickle(os.path.join(ROOT, 'out', 'cache', 'desc.pkl')).set_index('caseid')
    c = pd.read_pickle(os.path.join(ROOT, 'data', 'cohort_raw.pkl')).set_index('caseid')
    x = d[['art_pre_nibp', 'art_else', 'nibp_events']].dropna().join(c.aline1)
    x['site'] = np.where(x.aline1.str.contains('radial', na=False), 'radial',
                         np.where(x.aline1.str.contains('pedis|femoral', na=False), 'pedal/femoral', 'other'))
    x['side'] = x.aline1.str.split().str[0]
    x['excess'] = x.art_pre_nibp - x.art_else
    share = ('art_pre_nibp', lambda v: (v >= 0.1).mean())
    print(x.groupby('site').agg(n=('art_pre_nibp', 'size'), pre=('art_pre_nibp', 'mean'),
                                other=('art_else', 'mean'), share_ge10=share).round(3))
    print(x[x.site == 'radial'].groupby('side').agg(n=('art_pre_nibp', 'size'), pre=('art_pre_nibp', 'mean'),
                                                     share_ge10=share).round(3))
    print(mannwhitneyu(x[x.site == 'radial'].excess, x[x.site == 'pedal/femoral'].excess))
    x.to_csv(os.path.join(ROOT, 'out', 'descriptive', 'c3_by_site.csv'))
    import json
    site = x.groupby('site').agg(n=('art_pre_nibp', 'size'), pre=('art_pre_nibp', 'mean'),
                                 other=('art_else', 'mean'), share_pts_pre_ge10=share)
    side = x[x.site == 'radial'].groupby('side').agg(n=('art_pre_nibp', 'size'), pre=('art_pre_nibp', 'mean'),
                                                     share_pts_pre_ge10=share)
    mw = mannwhitneyu(x[x.site == 'radial'].excess, x[x.site == 'pedal/femoral'].excess)
    with open(os.path.join(ROOT, 'out', 'posthoc_review', 'cuff_site.json'), 'w') as fh:
        json.dump(dict(site=site.to_dict('index'), side=side.to_dict('index'),
                       mannwhitney_radial_vs_pedal_femoral_excess=dict(U=float(mw.statistic), p=float(mw.pvalue)),
                       note='per-patient means of the artefact fraction in the 60 s before cuff readings (pre) and '
                            'at other times (other); share_pts_pre_ge10: share of patients whose pre-cuff windows '
                            'were >= 10% artefact'), fh, indent=1)
