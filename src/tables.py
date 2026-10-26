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
RNAME = {'R1': 'R1', 'R2': 'R2', 'R3': 'R3', 'R4': 'R4', 'R5': 'R5'}
FNAME = {f'F{i}': f'F{i}' for i in range(7)}


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
            ('BMI, kg m^−2^', lambda g: med_iqr(g.bmi, 1)),
            ('ASA physical status ≥ 3', lambda g: pct(g.asa >= 3)),
            ('Emergency surgery', lambda g: pct(g.emop == 1)),
            ('Hypertension', lambda g: pct(g.preop_htn == 1)),
            ('Diabetes', lambda g: pct(g.preop_dm == 1)),
            ('Baseline eGFR, mL min^−1^ 1.73 m^−2^', lambda g: med_iqr(g.egfr)),
            ('Preoperative haemoglobin, g dL^−1^', lambda g: med_iqr(g.preop_hb, 1)),
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
    out = ['| F | R | Spurious % | Masked % | Exposed % P / R | κ | ROR (95% CI) | Simult. band |',
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
            cells.append(f'{100 * x.p_flagged:.0f} ({100 * x.lo:.0f}–{100 * x.hi:.0f}) [{x.episodes}]')
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
    PH = os.path.join(ROOT, 'out', 'posthoc_review')
    st = json.load(open(os.path.join(PH, 'stats.json')))
    tost = json.load(open(os.path.join(PH, 'tost.json')))
    thr = json.load(open(os.path.join(PH, 'thresholds.json')))
    mod = json.load(open(os.path.join(PH, 'models.json')))
    o2 = pd.read_csv(os.path.join(DESC, 'o2_spurious.csv'))
    o3 = pd.read_csv(os.path.join(DESC, 'o3_misclassification.csv'))
    out = ['# Supplementary tables\n',
           '## Table S1. Recorded minutes with MAP < 65 mmHg classified against the reference (descriptive cohort)\n',
           md(o2[['res', 'filter', 'low_min', 'spurious_frac', 'lo', 'hi', 'confirmed_frac', 'bridged_low_frac',
                  'indeterminate_frac', 'patients_with_spurious']]),
           '\nlow_min: pipeline minutes < 65; fractions are of low_min; lo/hi: patient-cluster bootstrap 95% CI '
           'of the spurious fraction.\n',
           '## Table S2. Agreement of the binary exposure (≥ 10 min MAP < 65) with the reference (descriptive cohort)\n',
           md(o3[['filter', 'res', 'prev_ref', 'prev_pipe', 'sens', 'spec', 'kappa', 'flips', 'up', 'down',
                  'mean_diff', 'loa_lo', 'loa_hi']]),
           '\nflips: patients whose category differs (up: exposed by pipeline only). R4/R5 at phase offset 0. '
           'mean_diff and limits of agreement in minutes below 65 mmHg.\n']
    rt = pd.read_csv(os.path.join(PH, 'realtime_table.csv'))
    out += ['## Table S3. POST HOC: probability that an episode is waveform-flagged, by elapsed time and nadir so far\n',
            md(rt.rename(columns={'elapsed_s': 'still < 65 mmHg after (s)'})),
            '\nAmong episodes that had lasted at least the stated time; nadir so far = lowest monitor MAP up to that time.\n']
    ph = pd.read_csv(os.path.join(RES, 'posthoc_depth.csv'))
    rows = [dict(item=k, value=v) for k, v in thr.items() if not isinstance(v, dict)]
    rows += [dict(item=k, value=f"ROR {v['ror']:.2f} ({v['lo']:.2f}–{v['hi']:.2f})") for k, v in thr.items() if isinstance(v, dict)]
    out += ['## Table S4. POST HOC: depth-weighted exposures and lower thresholds (1-min median resolution)\n',
            md(ph), '', md(pd.DataFrame(rows)),
            '\nTWA per mmHg; AUC (area under the threshold) per 100 mmHg·min, capped at the reference 99th centile. '
            'excess_share: fraction of the pipeline total area in excess of the reference total; top1pct_share: share of '
            'that excess contributed by the 1% of patients with the largest excess. Intervals as in A15.\n']
    sens = pd.read_csv(os.path.join(RES, 'sensitivity.csv'))
    extra = pd.DataFrame([dict(analysis=k, ror=v['ror'], lo=v['lo'], hi=v['hi'], events=v['events'])
                          for k, v in st['sensitivity'].items()])
    out += ['## Table S5. Sensitivity analyses of the primary ROR (F1 × R3)\n',
            md(pd.concat([sens, extra], ignore_index=True)),
            '\nRows from the frozen run first; S4, S6 (pre-specified, run after unblinding) and post hoc rows after. '
            'Rows without lo/hi are point estimates.\n']
    rows = []
    for spec, v in S['o5'].items():
        for model, xs in v['models'].items():
            for i, d in enumerate(xs):
                rows.append(dict(pipeline=spec, model=model, term=i, nonzero=d['nonzero'],
                                 or_per_sd=d['or_per_sd'], lo=d['lo_sd'], hi=d['hi_sd'],
                                 or_per_log1p=d['or_per_log1p'], lo_u=d['lo'], hi_u=d['hi']))
    for name, d in st['o5_separate_models_F0xR1'].items():
        rows.append(dict(pipeline='F0xR1 (separate model)', model=name, term=0, nonzero=None, or_per_sd=d['or_per_sd'],
                         lo=d['lo_sd'], hi=d['hi_sd'], or_per_log1p=d['or_per_log1p'], lo_u=d['lo'], hi_u=d['hi']))
    out += ['## Table S6. Differential misclassification: AKI on spurious minutes per hour, adjusted for reference exposure\n',
            md(pd.DataFrame(rows)),
            '\nterm 0: log(1 + spurious min/h) (or group-specific version); c_negative_control term 1: spurious '
            'hypertensive min/h; d_mechanism terms 1–3: blood gases/h, log blood loss, red-cell units. lo/hi per SD; '
            'lo_u/hi_u per unit of log(1 + min/h).\n']
    dsc = st['discordant']
    byk = json.load(open(os.path.join(PH, 'ror_by_k.json')))
    pb = byk[-1]['poisson_binomial_up']
    rows = [dict(pipeline=k, up=v['up'], aki_up=v['aki_up'], down=v['down'], aki_down=v['aki_down'])
            for k, v in dsc.items() if isinstance(v, dict) and 'up' in v]
    out += ['## Table S7. Discordant patients, operating characteristics of the equivalence decision, and interval coverage\n',
            md(pd.DataFrame(rows)),
            f"\nF1 × R3: expected AKI among the 33 discordant patients {dsc['F1xR3_expected_aki']:.2f}; "
            f"probability of none {dsc['F1xR3_p_k0']:.2f}.\n",
            md(pd.DataFrame([r for r in byk if 'k' in r])),
            '\nROR and A15 interval if k of the 28 upward-moved patients had developed AKI (outcomes swapped with k '
            'concordant cases; 400 bootstrap resamples, 200 permutations). Under the reference model, '
            f"P(k = 0) = {pb['p_k0']:.2f}, P(k = 1) = {pb['p_k1']:.2f}, P(k ≥ 2) = {pb['p_k_ge2']:.2f}.\n",
            md(pd.DataFrame([dict(scenario=k, **v) for k, v in tost.items() if isinstance(v, dict) and 'n' in v])),
            '\nSimulated outcomes from the fully adjusted reference model; differential error added as a log-odds '
            'shift γ in upward-moved patients. Each dataset analysed with the A15 rule (200 bootstrap resamples, '
            '200 permutations). Median ROR by γ: ' + ', '.join(f'{k}: {v:.2f}' for k, v in tost['median_ror_by_gamma'].items())
            + '. Coverage of 1 under independent permutations (SD from the dry run, 100 calibration datasets): '
            + ', '.join(f"{k} {v['coverage']:.2f}" for k, v in st['calibrated_coverage_independent'].items()) + '.\n']
    sw = pd.read_csv(os.path.join(ROOT, 'out', 'v1_sweep.csv'))
    swt = sw.groupby(['kind', 'param'], sort=False)[['any_artefact', 'frac_artefact']].mean().reset_index()
    out += ['## Table S8. Injection–recovery sweep (post hoc)\n', md(swt),
            '\nany_artefact: share of injections with at least one window in the injected 20 s labelled artefact '
            '(zero/high/non-pulsatile/noise; guard excluded); 119 clean 2-min segments from 60 cases.\n']
    ai = json.load(open(os.path.join(ROOT, 'out', 'adjudication', 'ai_rater_agreement.json')))
    out += ['## Table S9. Blinded AI rating of 152 snippets (secondary)\n',
            md(pd.DataFrame([ai]).T.reset_index().rename(columns={'index': 'item', 0: 'value'})), '']
    m = S['mortality']
    out += ['## Table S10. In-hospital mortality (exploratory, reduced adjustment set)\n',
            f"n = {m['n']}, deaths = {m['deaths']}; OR reference {m['or_ref']:.2f} ({m['or_ref_ci'][0]:.2f}–{m['or_ref_ci'][1]:.2f}); "
            f"OR F1 × R3 {m['or_pipe']:.2f} ({m['or_pipe_ci'][0]:.2f}–{m['or_pipe_ci'][1]:.2f}); ROR {m['ror']:.2f}.\n"]
    rows = []
    for series in ('reference', 'F1xR3'):
        for expo, v in mod[series].items():
            for lvl, d in v.items():
                rows.append(dict(series=series, exposure=expo, adjustment=lvl, odds_ratio=d['or_'], lo=d['lo'], hi=d['hi']))
    out += ['## Table S11. Odds ratios for AKI by adjustment level (AKI set, 1-min median)\n', md(pd.DataFrame(rows)),
            '\nreduced_set: age and eGFR splines, ASA ≥ 3, emergency. Wald intervals from Firth fits. AKI-set inclusion by '
            'department: ' + ', '.join(f"{k} {v['mean']:.0%} of {v['size']}" for k, v in mod['aki_set_by_department'].items()) + '.\n']
    return '\n'.join(out)

if __name__ == '__main__':
    big = ['## Table 3. Every filter × resolution: measurement error and its effect on the AKI association\n',
           table2(),
           '\nF, filter: F0 none; F1 MAP 20–250; F2 MAP 30–200; F3 Jacobsson rule; F4 physiological consistency; F5 F4 + neighbour rule; F6 F4 + 7-point running median. R, resolution: R1 2-s stream; R2 one instantaneous value per minute; R3 1-min median; R4 5-min chart; R5 15-min chart. P / R, pipeline / reference. Spurious: pipeline minute < 65 mmHg with reference ≥ 65. Masked: share of reference minutes < 65 that the '
           'pipeline records ≥ 65; neither is defined for charted resolutions. '
           'Exposure: ≥ 10 min with MAP < 65 mmHg; exposure prevalence and κ from the descriptive cohort '
           '(charted resolutions at phase offset 0). ROR (ratio of odds ratios, pipeline / reference at matched '
           'resolution) from the AKI set; 95% CI = log ROR ± 1.96 × max(paired-bootstrap SE, permutation-null SD); '
           'simultaneous band: bootstrap max-|z| critical value over all 35 cells applied to the same SE.\n']
    parts = ['## Table 1. Patient characteristics\n', table1(),
             '\nValues are median (IQR) or n (%). Reference = waveform-referenced monitor MAP, 1-min median.\n',
             '## Table 2. Probability that a recorded low-MAP episode is waveform-flagged artefact\n',
             table3(),
             '\nEpisode: contiguous run of monitor MAP < 65 mmHg. Cells: % flagged (patient-cluster bootstrap 95% CI) '
             '[number of episodes].\n'] + big
    supp = supplementary()
    with open(os.path.join(ROOT, 'paper', f'supplement_tables{"" if MODE == "real" else "_" + MODE}.md'), 'w') as fh:
        fh.write(supp)
    path = os.path.join(ROOT, 'paper', f'tables{"" if MODE == "real" else "_" + MODE}.md')
    with open(path, 'w') as fh:
        fh.write('\n'.join(parts))
    print(path)
