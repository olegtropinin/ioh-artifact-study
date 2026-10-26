"""Manuscript tables (markdown) from the analysis outputs.

python src/tables.py real   -> paper/tables.md
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from analysis import descriptive_cohort          # noqa: E402
from models import cohort, load_outcome           # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODE = sys.argv[1] if len(sys.argv) > 1 else 'real'
RES = os.path.join(ROOT, 'out', f'results_{MODE}')
DESC = os.path.join(ROOT, 'out', 'descriptive')
RNAME = {'R1': '2-s stream', 'R2': '1 value/min', 'R3': '1-min median', 'R4': '5-min chart', 'R5': '15-min chart'}
FNAME = {'F0': 'F0 none', 'F1': 'F1 MAP 20–250', 'F2': 'F2 MAP 30–200', 'F3': 'F3 Jacobsson',
         'F4': 'F4 consistency', 'F5': 'F5 F4 + neighbour', 'F6': 'F6 F4 + 7-pt median'}


def med_iqr(x, d=0):
    q = np.nanpercentile(x, [50, 25, 75])
    return f'{q[0]:.{d}f} ({q[1]:.{d}f}–{q[2]:.{d}f})'


def pct(x):
    return f'{np.nansum(x):.0f} ({100 * np.nanmean(x):.1f})'


def table1():
    d = descriptive_cohort()
    a, _ = cohort()
    y = load_outcome(a, MODE)
    groups = [('Descriptive cohort', d), ('AKI set: no AKI', a[y == 0]), ('AKI set: AKI', a[y == 1])]
    rows = [('n', lambda g: f'{len(g)}'),
            ('Age, years', lambda g: med_iqr(g.age)),
            ('Female', lambda g: pct(g.sex == 'F')),
            ('BMI, kg m⁻²', lambda g: med_iqr(g.bmi, 1)),
            ('ASA physical status ≥ 3', lambda g: pct(g.asa >= 3)),
            ('Emergency surgery', lambda g: pct(g.emop == 1)),
            ('Hypertension', lambda g: pct(g.preop_htn == 1)),
            ('Diabetes', lambda g: pct(g.preop_dm == 1)),
            ('Baseline eGFR, mL min⁻¹ 1.73 m⁻²', lambda g: med_iqr(g.egfr)),
            ('Preoperative haemoglobin, g dL⁻¹', lambda g: med_iqr(g.preop_hb, 1)),
            ('General surgery', lambda g: pct(g.department == 'General surgery')),
            ('Thoracic surgery', lambda g: pct(g.department == 'Thoracic surgery')),
            ('Gynaecology / urology', lambda g: pct(g.department.isin(['Gynecology', 'Urology']))),
            ('Open approach', lambda g: pct(g.approach == 'Open')),
            ('Anaesthesia duration, h', lambda g: med_iqr(g.ane_dur_h, 1)),
            ('Monitored time, min', lambda g: med_iqr(g.period_min)),
            ('Reference minutes MAP < 65 mmHg', lambda g: med_iqr(ref_minutes(g))),
            ('Reference ≥ 10 min MAP < 65 mmHg', lambda g: pct(ref_minutes(g) >= 10))]
    out = ['| Characteristic | ' + ' | '.join(n for n, _ in groups) + ' |',
           '|---|' + '---|' * len(groups)]
    for name, fn in rows:
        out.append(f'| {name} | ' + ' | '.join(fn(g) for _, g in groups) + ' |')
    return '\n'.join(out)


_REF = None


def ref_minutes(g):
    global _REF
    if _REF is None:
        x = pd.read_pickle(os.path.join(ROOT, 'out', 'cache', 'exposures.pkl'))
        _REF = x[(x.family == 'ref') & (x['filter'] == 'bridged') & (x.res == 'R3') & (x.offset == 0)
                 & (x.thr == 65)].set_index('caseid')['minutes']
    return _REF.reindex(g.index).to_numpy(float)


def table2():
    """The big table: every filter x resolution, prevalence, agreement and ROR."""
    r = pd.read_csv(os.path.join(RES, 'ror_binary_FxR.csv'))
    o3 = pd.read_csv(os.path.join(DESC, 'o3_misclassification.csv'))
    o2 = pd.read_csv(os.path.join(DESC, 'o2_spurious.csv'))
    m = r.merge(o3, on=['filter', 'res'], how='left').merge(
        o2.assign(masked_of_true=o2.masked_min / (o2.masked_min + (o2.confirmed_frac + o2.bridged_low_frac) * o2.low_min))[
            ['filter', 'res', 'spurious_frac', 'masked_of_true']], on=['filter', 'res'], how='left')
    out = ['| Filter | Resolution | Spurious % of low minutes | Masked % | Exposed, pipeline / reference % | κ | ROR (95% CI) | Simultaneous band |',
           '|---|---|---|---|---|---|---|---|']
    for _, x in m.iterrows():
        sp = '–' if pd.isna(x.spurious_frac) else f'{100 * x.spurious_frac:.1f}'
        ms = '–' if pd.isna(x.masked_of_true) else f'{100 * x.masked_of_true:.1f}'
        out.append(f'| {FNAME[x["filter"]]} | {RNAME[x.res]} | {sp} | {ms} | '
                   f'{100 * x.prev_pipe:.1f} / {100 * x.prev_ref:.1f} | {x.kappa:.2f} | '
                   f'{x.ror:.2f} ({x.ror_lo:.2f}–{x.ror_hi:.2f}) | {x.ror_simlo:.2f}–{x.ror_simhi:.2f} |')
    return '\n'.join(out)


def table3():
    t = pd.read_csv(os.path.join(DESC, 'o6_probability_table.csv'))
    durs = list(dict.fromkeys(t.duration))
    nads = list(dict.fromkeys(t.nadir))
    out = ['| Nadir \\ duration | ' + ' | '.join(durs) + ' |', '|---|' + '---|' * len(durs)]
    for n in nads:
        cells = []
        for d in durs:
            x = t[(t.duration == d) & (t.nadir == n)].iloc[0]
            cells.append(f'{100 * x.p_flagged:.0f}% ({100 * x.lo:.0f}–{100 * x.hi:.0f}); n = {x.episodes}')
        out.append(f'| {n} mmHg | ' + ' | '.join(cells) + ' |')
    return '\n'.join(out)


def md(df, fmt=3):
    df = df.copy()
    for col in df.columns:
        if df[col].dtype.kind == 'f':
            df[col] = df[col].map(lambda v: '' if pd.isna(v) else f'{v:.{fmt}g}' if abs(v) >= 1000 else f'{v:.{fmt}f}')
    head = '| ' + ' | '.join(map(str, df.columns)) + ' |'
    return '\n'.join([head, '|' + '---|' * len(df.columns)] +
                     ['| ' + ' | '.join(map(str, r)) + ' |' for r in df.itertuples(index=False)])


def supplementary():
    S = json.load(open(os.path.join(RES, 'summary.json')))
    o2 = pd.read_csv(os.path.join(DESC, 'o2_spurious.csv'))
    o3 = pd.read_csv(os.path.join(DESC, 'o3_misclassification.csv'))
    ph_path = os.path.join(RES, 'posthoc_depth.csv')
    out = ['# Supplementary tables\n',
           '## Table S1. Classification of recorded minutes with MAP < 65 mmHg against the reference (descriptive cohort)\n',
           md(o2[['res', 'filter', 'low_min', 'spurious_frac', 'lo', 'hi', 'confirmed_frac', 'bridged_low_frac',
                  'indeterminate_frac', 'masked_per_low', 'patients_with_spurious']]),
           '\nlow_min: pipeline minutes < 65; fractions are of low_min; lo/hi: patient-cluster bootstrap 95% CI of the '
           'spurious fraction; masked_per_low: reference low minutes recorded ≥ 65 by the pipeline, per pipeline low minute.\n',
           '## Table S2. Agreement of the binary exposure (≥ 10 min MAP < 65) with the reference\n',
           md(o3[['filter', 'res', 'prev_ref', 'prev_pipe', 'sens', 'spec', 'kappa', 'flips', 'up', 'down',
                  'mean_diff', 'loa_lo', 'loa_hi']]),
           '\nflips: patients whose exposure category differs (up: unexposed by reference, exposed by pipeline). '
           'mean_diff and limits of agreement (loa) in minutes below 65 mmHg.\n']
    if os.path.exists(ph_path):
        out += ['## Table S3. POST HOC: calibrated RORs for depth-weighted exposures (1-min median resolution)\n',
                md(pd.read_csv(ph_path)),
                '\nTWA per mmHg; AUC per 100 mmHg·min (capped at the reference 99th centile). Not pre-specified.\n']
    out += ['## Table S4. Sensitivity analyses of the primary ROR (F1 × R3)\n',
            md(pd.read_csv(os.path.join(RES, 'sensitivity.csv'))), '']
    rows = []
    for spec, v in S['o5'].items():
        for model, xs in v['models'].items():
            for i, d in enumerate(xs):
                rows.append(dict(pipeline=spec, model=model, term=i, nonzero=d['nonzero'],
                                 or_per_sd=d['or_per_sd'], lo=d['lo_sd'], hi=d['hi_sd']))
    out += ['## Table S5. Differential misclassification: AKI on spurious minutes per hour, adjusted for reference exposure\n',
            md(pd.DataFrame(rows)),
            '\nterm 0: log(1 + spurious min/h) (or the group-specific version); c_negative_control term 1: spurious '
            'hypertensive min/h; d_mechanism terms 1–3: blood gases/h, log blood loss, red-cell units. Odds ratios per SD.\n']
    return '\n'.join(out)


if __name__ == '__main__':
    big = ['## Table 3. Every filter × resolution: measurement error and its effect on the AKI association\n',
           table2(),
           '\nSpurious: pipeline minute < 65 mmHg with reference ≥ 65. Masked: share of reference minutes < 65 that the '
           'pipeline records ≥ 65; neither is defined for charted resolutions. '
           'Exposure: ≥ 10 min with MAP < 65 mmHg; exposure prevalence and κ from the descriptive cohort '
           '(charted resolutions at phase offset 0). ROR (ratio of odds ratios, pipeline / reference at matched '
           'resolution) from the AKI set; 95% CI = log ROR ± 1.96 × max(paired-bootstrap SE, permutation-null SD); '
           'simultaneous band: bootstrap max-|z| critical value over all 35 cells applied to the same SE.\n']
    parts = ['## Table 1. Patient characteristics\n', table1(),
             '\nValues are median (IQR) or n (%). Reference = waveform-verified monitor MAP, 1-min median.\n',
             '## Table 2. Probability that a recorded low-MAP episode is waveform-flagged artefact\n',
             table3(),
             '\nEpisode: contiguous run of monitor MAP < 65 mmHg. Percent flagged (patient-cluster bootstrap 95% CI); '
             'n = episodes.\n'] + big
    supp = supplementary()
    with open(os.path.join(ROOT, 'paper', f'supplement_tables{"" if MODE == "real" else "_" + MODE}.md'), 'w') as fh:
        fh.write(supp)
    path = os.path.join(ROOT, 'paper', f'tables{"" if MODE == "real" else "_" + MODE}.md')
    with open(path, 'w') as fh:
        fh.write('\n'.join(parts))
    print(path)
