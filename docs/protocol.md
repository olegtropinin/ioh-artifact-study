# Analysis protocol (frozen before any outcome analysis)

**Working title.** How much of recorded intraoperative hypotension is artefact, and how much does
it matter? A waveform-referenced multiverse analysis of arterial-line artefacts, data resolution
and the hypotension–acute kidney injury association in VitalDB.

**Status at freezing.** Window features extracted from the 500 Hz arterial waveform; artefact
classifier inspected visually on 20 snippets and descriptive artefact burden computed on ≤ 600
cases. **No association between any exposure and any outcome has been computed.** The freeze
is the git commit containing this file; any later change is recorded in the "Amendments"
section with date and reason.

Reporting: STROBE and RECORD. Design: retrospective cohort, secondary analysis of a
de-identified open dataset.

## 1. Objectives

| # | Objective | Type |
|---|---|---|
| O1 | Artefact burden of the intraoperative arterial line, by artefact type | descriptive |
| O2 | Fraction of *recorded* hypotensive minutes that are artefact, for each processing pipeline | descriptive (primary measurement endpoint) |
| O3 | Per-patient misclassification of hypotension exposure versus the reference | descriptive |
| O4 | How the adjusted association between hypotension and AKI changes across pipelines (multiverse / specification curve) | **primary inferential** |
| O5 | Differential misclassification: is artefact-attributable "hypotension" associated with blood-gas sampling, severity and AKI? | secondary, hypothesis-driven |
| O6 | Probability that a low monitor MAP episode is artefact, by duration and nadir; a simple bedside rule, derived and validated on separate patients | secondary, clinical |

## 2. Data and cohort

VitalDB (Seoul National University Hospital, 2016–2017; Lee HC et al., Sci Data 2022). Open,
de-identified; original collection approved by the SNUH IRB. No new ethics approval needed
(to be confirmed against the VitalDB data-use terms and stated in the paper).

Inclusion: `SNUADC/ART` waveform present; age ≥ 18; general anaesthesia; ≥ 30 min of
monitoring period (definition §3).
Exclusions for the AKI analysis: missing baseline creatinine; baseline eGFR < 15 (proxy for
end-stage renal disease); no creatinine within 7 days after the end of anaesthesia;
transplantation procedures (`optype == 'Transplantation'`; included in sensitivity S6).

## 3. Reference series (waveform-informed)

- 2-s windows of the 500 Hz waveform are labelled `valid`, `missing`, `zero`, `high`,
  `nonpulsatile`, `noise` (rules in `src/artifact.py`, frozen at this commit), plus `guard`:
  windows within 10 s of any non-valid window.
- The monitor's 2-s ART_MBP numerics are aligned to the waveform by a per-case lag (1–4
  samples, maximum correlation on valid windows).
- **Reference minute MAP** = median of the aligned monitor MAP values in `valid` windows of the
  minute, if ≥ 50% of the minute's windows are valid; otherwise missing.
- Rationale: the reference differs from the monitor stream only by removal of
  waveform-detected artefact, so calibration differences between the monitor and the ADC do
  not enter the comparison.
- **Monitoring period** = from the first to the last run of ≥ 60 s of valid windows within
  anaesthesia (anestart–aneend). All pipelines use the same period.

## 4. Pipelines (the multiverse)

Pipelines use **only the monitor numerics** (MAP, SBP, DBP), as a retrospective study would.

**Filter** (applied to 2-s numerics; F5 and F6 after sampling, see A8):

| Code | Rule | Source |
|---|---|---|
| F0 | none | — |
| F1 | drop MAP < 20 or > 250 | Lee 2026 (VitalDB AKI) |
| F2 | drop MAP < 30 or > 200 | Khan 2022 |
| F3 | drop SBP > 250, DBP < 15, MAP < 35 or > 150, SBP−DBP < 15 | Jacobsson 2026 |
| F4 | drop MAP < 20 or > 200, SBP > 300 or < 20, SBP ≤ DBP, SBP−DBP < 5, DBP < 5 | physiological consistency |
| F5 | F4 + drop values differing from both neighbours by > 30 mmHg | neighbour comparison (Du 2019 style) |
| F6 | F4 + 7-point running median on the minute grid | median filter (Pasma 2020) |

**Resolution:** R1 2-s (all values; minutes = count × 2 s / 60); R2 1-min instantaneous
(value at the minute mark); R3 1-min median; R4 5-min instantaneous, held; R5 15-min
instantaneous, held.

**Metric:** cumulative minutes < T; area under T (mmHg·min); time-weighted average below T
(AUC / monitored minutes); binary "≥ 10 cumulative minutes < T".
**Threshold:** T ∈ {55, 60, 65} mmHg.

7 × 5 × 4 × 3 = **420 pipeline specifications**, each compared with the reference computed
with the same metric and threshold (12 reference specifications).

## 5. Outcomes and covariates

- **Primary:** AKI by KDIGO creatinine criteria within 7 days (≥ 0.3 mg/dL within 48 h, or
  ≥ 1.5× baseline within 7 days). Baseline = last creatinine within 30 days before induction,
  else `preop_cr`. Urine output not available postoperatively.
- **Secondary:** AKI stage ≥ 2; in-hospital death.
- **Adjustment set (fixed):** age, sex, BMI, ASA ≥ 3, emergency, baseline eGFR (CKD-EPI
  2021), hypertension, diabetes, preoperative haemoglobin, preoperative albumin, department,
  surgical approach, log anaesthesia duration. Missing covariates: median (continuous) or
  mode (categorical) imputation with a missingness indicator if > 5% missing.
  Intraoperative vasopressors, fluids and blood loss are not adjusted for (potential
  mediators); sensitivity S5 adds blood loss.

## 6. Statistical analysis

- **O2.** Among pipeline-recorded minutes with MAP < 65: proportion where the reference minute
  is missing because of artefact, or ≥ 65. Reported per pipeline with patient-cluster
  bootstrap 95% CI (1,000 resamples).
- **O3.** For the binary exposure, sensitivity, specificity and Cohen's kappa against the
  reference. For minutes < 65, the median per-patient difference and Bland–Altman limits.
- **O4.**
  - For each of the 432 specifications, a logistic regression of AKI on the exposure plus
    the adjustment set.
  - Units:
    - binary: OR;
    - minutes: per 10 min, truncated at 120 min;
    - AUC: per 100 mmHg·min, truncated at the 99th percentile of the reference
      distribution;
    - TWA: per 1 mmHg.
  - **Primary estimand:** the ratio of odds ratios (ROR = OR_pipeline / OR_reference) for
    the binary exposure "≥ 10 min with MAP < 65", with patient-level paired bootstrap 95% CI
    (1,000 resamples, the same resample for both models).
  - Paired bootstrap for all 35 filter × resolution specifications of the primary metric.
    The other specifications are reported as point estimates in a specification curve.
  - Fragility summaries: range and IQR of ORs; proportion of specifications whose 95% CI
    excludes 1; the number of specifications that change the qualitative conclusion.
- **O5.**
  - Artefact-attributable minutes = minutes < 65 (F1, R3) − reference minutes < 65.
  - (a) Spearman correlation with the number of intraoperative arterial blood gases (VitalDB
    labs with a pH result during anaesthesia) and with ASA.
  - (b) Logistic regression of AKI on artefact-attributable minutes, adjusted for reference
    minutes and the adjustment set. Any association indicates differential
    misclassification.
- **O6.**
  - Episodes are contiguous runs of aligned 2-s monitor MAP < 65 within the monitoring
    period.
  - An episode is **artefactual** if ≥ 50% of its windows are non-valid (any label other
    than `valid`, including `guard`).
  - P(artefact) is tabulated by duration (≤ 10 s, 10–30 s, 30–60 s, 1–2 min, 2–5 min, > 5 min)
    × nadir (< 20, 20–39, 40–54, 55–64), with Wilson CIs.
  - A simple rule is derived on a 50% patient split (hash of caseid) and validated on the
    other 50%. The rule uses only features visible at the bedside: duration, nadir, and the
    maximum MAP in the preceding 30 s.
- **Mortality** (few events, about 40): Firth-penalised logistic regression adjusted for age,
  ASA ≥ 3, emergency and eGFR. Reported descriptively with the specification spread only.

## 7. Validation of the reference

- **V1 injection–recovery:**
  - Clean 2-min segments from 100 randomly selected cases.
  - Inject synthetic artefacts (Li, Mark & Clifford 2009 types): flush square wave to
    300 mmHg, zeroing (0 mmHg), sampling (flat line at line pressure, then flush), overdamping
    (low-pass), high-frequency noise, and a 15 mmHg transducer offset.
  - Report the detection sensitivity per type. Specificity is measured on uninjected clean
    segments.
  - The transducer offset is expected to be undetectable by design (limitation).
- **V2 blinded adjudication:** 150 stratified random 40-s snippets, plotted without labels and
  adjudicated by an independent AI reviewer agent as valid or artefact. Report kappa. The
  adjudicator is not a human expert, and this is disclosed.
- **V3 physiological concordance:** |ART − NIBP| at NIBP measurement times, for valid versus
  non-valid windows; agreement of the waveform HR with the monitor ECG HR.

## 8. Sensitivity analyses

| Code | Change |
|---|---|
| S1 | guard 0 s and 30 s |
| S2 | pulse-pressure threshold for non-pulsatile 5 and 12 mmHg |
| S3 | reference minute validity threshold 25% and 75% |
| S4 | missing postoperative creatinine treated as no AKI (cohort without the 7-day creatinine requirement) |
| S5 | add intraoperative blood loss to the adjustment set |
| S6 | include transplantation |
| S7 | AKI stage ≥ 2 |
| S8 | reference built on the waveform mean instead of the monitor numerics |

## 9. What this study cannot show

- It cannot detect artefacts that leave a normal-looking waveform, such as transducer
  height errors. The reference is an improved series, not ground truth.
- It cannot identify the clinical response to artefacts: VitalDB records vasopressor bolus
  totals only.
- The data come from a single centre in 2016–2017.
- The associations are observational.

## Amendments (2026-10-26, before freezing, after an adversarial methods review; no outcome data examined)

Where an amendment conflicts with the text above, the amendment governs.

**A1 (adapted) — validation without human adjudicators.** Two blinded human anaesthesiologist
adjudicators are not available for this version. Validation of the reference therefore
rests on (i) physiological concordance with independent sensors (V3, now primary),
(ii) injection–recovery (V1), and (iii) a blinded AI rater (V2, explicitly secondary and
non-decisive). Throughout the paper, minutes are called **"waveform-flagged"** rather than
"artefact" unless independent evidence supports the stronger term. A stratified 400-snippet
adjudication set (strata A–D of the review: 150 monitor MAP < 65 & non-valid incl. 50
guard-only; 100 MAP < 65 & valid; 100 random valid; 50 random non-valid with MAP ≥ 65; at
most two per patient, selected by hash of subjectid) is generated and released with blank
forms, so that human adjudication can be added later.

**A2 — freeze.** The freeze is a git tag `protocol-freeze` on a commit whose code implements
§4–§6 with these amendments, passes `tests/test_pipelines.py`, and has completed an
end-to-end run with the AKI and death vectors replaced by a seeded permutation (outputs
archived in `out/results_permuted/`). The SHA-256 of `src/*.py` is recorded in the tag
message. An external registry (OSF) was not available; the local git history is the record.
Descriptive artefact statistics before freezing used ≤ 600 cases.

**A3 — primary estimand.** ROR = OR_P / OR_ref for "≥ 10 cumulative minutes with MAP < 65",
P = F1 × R3 (MAP 20–250 range filter, 1-min median), ref = bridged reference at R3. Paired
bootstrap, 2,000 resamples of patients, percentile 95% CI. Decision rule with equivalence
margin 0.80–1.25: CI entirely within → "artefact handling does not materially change the
association"; CI excludes 1 and point estimate outside the margin → "material change";
otherwise "inconclusive". Under non-differential misclassification of plausible size the ROR
is expected near 0.90–0.97, so this estimand detects differential bias large enough to
matter. Key secondaries: (a) F0 × R1 vs ref@R1; (b) per-10-min log-OR for cumulative minutes
< 65, F1 × R3 vs ref@R3, difference with bootstrap CI and attenuation factor β_P/β_ref.

**A4 — gap bridging.** Runs of non-valid windows ≤ 3 min bounded by ≥ 30 s of valid windows on
both sides are linearly bridged between the median valid MAP of the 30 s before and after.
The unbridged reference is a sensitivity analysis. Each pipeline-recorded minute < 65 is
*spurious* (reference ≥ 65), *confirmed* (reference < 65, ≥ 50% observed), *bridged-low*
(reference < 65, < 50% observed) or *indeterminate* (reference missing). Primary O2 quantity
= spurious / all recorded minutes < 65, reported with indeterminate / all; indeterminate
minutes are never counted as artefact.

**A5 — missing waveform.** `missing` is not an artefact and creates no guard. Minutes with
> 50% `missing` windows are excluded from every pipeline and the reference (common support).

**A6 — patients.** Unit = patient (`subjectid`); first eligible case per patient (lowest
caseid). Bootstrap and the O6 split are by patient.

**A7 — O5.** (a) Spearman of spurious minutes per monitored hour with arterial blood gases per
hour and ASA. (b) Firth logistic regression of AKI on log1p(spurious minutes/h), adjusted for
reference minutes < 65 (linear + restricted cubic spline), log monitored hours and the §5 set;
separately for minutes dominated by zero/high labels (g1) and non-pulsatile/noise labels (g2).
(c) Negative-control exposure: spurious hypertensive minutes (pipeline MAP > 120 with
reference ≤ 100), in the same model. (d) Mechanism model adding blood gases per hour,
log1p(blood loss) and red-cell units.

**A8 — resolution.** The reference is sampled at every resolution and each pipeline is
compared with ref@R; the resolution effect is OR(ref@R)/OR(ref@R3). R4 uses all 5 phase
offsets and R5 offsets 0, 3, 6, 9, 12 min; log-ORs are averaged over offsets within each
bootstrap resample. A charted value is the first non-missing 2-s value in its interval. F5
and F6 are applied after sampling on the pipeline's own grid (F6 = 7-point running median).
S10: each pipeline uses a numerics-defined monitoring period (first to last 60-s run of
monitor MAP 40–150 within anaesthesia), as a retrospective study would.

**A9 — classifier calibration (descriptive data only).** Noise = waveform minimum < −10 mmHg or
median |second difference| ≥ 4 mmHg (the single-spike slope rule is dropped). Guard is
asymmetric: 2 s before and 8 s after each artefact run (95th centile of monitor recovery
time after zero/high/non-pulsatile runs = 8 s; 99th = 16 s). Sensitivity S1 uses 0/0 s and
6/30 s.

**A10 — physiological checks (V3, now primary validation).** (i) For monitor MAP < 65
episodes with an NIBP reading within ±3 min: proportion with NIBP MAP ≥ 70, by episode class;
(ii) for non-pulsatile windows: proportion with concurrent ECG HR 40–150 and pleth HR 40–150;
(iii) non-pulsatile fraction in patients with preoperative atrial fibrillation versus sinus
rhythm. V1 specificity is reported as the flag rate outside the injected stretch.

**A11 — O6.** Probability that a monitor-numerics low-MAP episode is waveform-flagged, for
retrospective cleaning and automated systems (not bedside use). Episode classes: *flagged*
(≥ 50% artefact labels), *guard-dominated* (artefact + guard ≥ 50%, artefact < 50%),
*physiological* (otherwise). Patient-cluster bootstrap CIs. Rule: depth-≤ 2 tree on duration,
nadir and maximum MAP in the preceding 30 s, derived on a 50% patient-hash split with leaves
called "flagged" only at ≥ 90% specificity; validated on the other half (sensitivity,
specificity, PPV with cluster CIs).

**A12 — models.** Age and eGFR as restricted cubic splines (3 knots). Firth-penalised
likelihood for all models; failures counted. Simultaneous 95% bands (bootstrap max-|z|) for
the 35 F × R RORs. One analysis set for all specifications. S7 and mortality use a reduced
set (age and eGFR splines, ASA ≥ 3, emergency). Mortality: one pre-specified specification
(primary P vs ref) in the descriptive cohort, exploratory, no specification curve. S11 adds
the number of postoperative creatinine measurements. Precision check before unblinding by
simulation with assumed (not estimated) covariate effects and OR_ref = 1.5; if the expected
95% CI half-width of log ROR exceeds 0.22, the equivalence conclusion is declared
unattainable in advance.

**Cohorts.** *Descriptive cohort* (O1–O3, O6, V3, mortality): adults, general anaesthesia,
≥ 30 min reference-valid monitoring, first case per patient. *AKI analysis set* (O4, O5,
S-analyses): additionally excludes transplantation, missing baseline creatinine, eGFR < 15,
and no creatinine within 7 days.

**A13 — classifier v2 (before freezing; no outcome data examined).** The beat-lag
autocorrelation pulsatility criterion was dropped: in descriptive data it labelled 12% of
windows in patients with preoperative atrial fibrillation as non-pulsatile (1% in sinus
rhythm), and those windows had pulse pressures of 56–83 mmHg; it also fired on bigeminy and
slow heart rates. It was replaced by: pulse pressure < 8 mmHg, OR interdecile range < 3 mmHg,
OR no systolic upstroke (rise > 8 mmHg within 100 ms) in the centred 6-s window. The noise
rule became minimum < −10 mmHg OR median absolute second difference ≥ 4 mmHg (the earlier
rule fired on single spikes). Guard is asymmetric: 2 s before and 8 s after an artefact run
(95th centile of monitor recovery). All 3,645 waveform cases were re-extracted with these
features; 211 had a waveform track listed but not retrievable and are excluded as "waveform
not retrievable".

**A14 — O5 power and Firth iterations (before freezing; only the permuted outcome examined).**
In the permuted dry run, spurious minutes at F1 × R3 were non-zero in 241 of 2,563 patients
(zero/flush-dominated in 19), which cannot carry the differential-misclassification test.
O5 is therefore run twice: at F1 × R3 as pre-specified, and at F0 × R1 (raw 2-s stream;
non-zero in 1,728 patients), with odds ratios also reported per standard deviation of the
exposure. The F0 × R1 version is the one interpreted. The Firth iteration limit was raised
from 50 to 200: in the dry run 1.7% of bootstrap fits stopped at 50 iterations short of the
1e−7 tolerance, and refitting them changed the estimate only in the eighth decimal.

**A15 — null calibration of the ROR interval (written before the calibration result was
seen; real outcome never examined).** In the dry run several RORs had percentile intervals
excluding 1 although the permuted outcome makes the true ROR exactly 1, because the contrast
rests on the few dozen patients whose exposure category differs. `src/null_calibration.py`
re-permutes the outcome 100 times and, for F1 × R3, F0 × R1, F3 × R2 and F6 × R3, records how
often the paired-bootstrap 95% interval (B = 200) covers 1, and the ratio of the mean
bootstrap SE to the SD of log ROR across permutations. Decision rule, fixed now:
- if coverage for F1 × R3 is ≥ 0.90, the percentile bootstrap interval stays primary;
- otherwise every ROR interval (and simultaneous band) is computed as
  log ROR ± z × max(bootstrap SE, permutation-null SD of that cell), with the null SD
  estimated by 200 permutations per cell, and the percentile interval is reported as
  secondary. The equivalence verdict uses the primary interval.

*A15 result (100 permutations, B = 200).* Coverage of 1 by the percentile interval: F1 × R3
0.51, F0 × R1 0.79, F3 × R2 0.89, F6 × R3 0.91. The bootstrap distribution of log ROR is
spiky — most resamples change few of the patients who drive the contrast — so its central
95% is narrow even where its SD is not (mean bootstrap SE / null SD 0.80 for F1 × R3). The
pre-specified rule therefore applies: primary intervals are log ROR ± z × max(bootstrap SE,
permutation-null SD), with 200 permutations per cell. Under the same 100 null permutations
this interval covered 1 in 0.99, 0.99, 1.00 and 0.97 respectively (conservative). The rule
is applied to all ROR-type contrasts: the 35 F × R cells and their simultaneous bands, the
resolution effect, the dose-slope differences and the reference-variant sensitivity analyses.

## Notes after unblinding

**Code hash.** The `protocol-freeze` tag message records the SHA-256 printed by the final
permuted dry run (12375fea…). Between that dry run and the freeze commit, only
`src/figures.py` and `src/tables.py` (plotting and table formatting) were edited, so the
hash of `src/*.py` at the tagged commit is 871bd97e…, which is the hash recorded by the real
analysis (`out/results_real/summary.json`). `git diff protocol-freeze -- src/analysis.py
src/models.py src/pipelines.py src/artifact.py` is empty for the real run.

**Post hoc (not pre-specified).** `src/posthoc_depth.py` adds A15-calibrated intervals for
the depth-weighted RORs (AUC and TWA below 55 and 65 mmHg, F0/F1/F3 at R3), prompted by
their point estimates in the specification curve. Reported as post hoc. The depth-metric
heatmap (Figure 3) and forest plot (Figure 6) were added after unblinding.

**Post hoc (not pre-specified).** `src/posthoc_cuff_site.py` compares the peri-cuff artefact
excess between radial and pedal/femoral catheters (an arm cuff cannot occlude the latter) and
between right and left radial catheters, prompted by the C3 result.

**Round-1 review changes (2026-10-26, after unblinding).** Three AI peer reviewers
(statistics, clinical anaesthesia, signal processing/reproducibility; `docs/reviews/`) led to:
- *Cuff timing fixed.* `n_NIBP_MBP` had been shifted by the arterial-numerics lag
  (pipelines.py, figures.py). Cuff values are not delayed like the arterial numerics, so the
  shift was removed. This affects only C3, V3 and Figure 2 (outcome-free). The primary
  reference was re-checked after re-running `run_all.py`: OR_ref and OR_pipe for F1 × R3 are
  identical to the frozen run (0.9403 and 0.8992).
- *Reference variants added (sensitivity only; primary unchanged).* `valid25_obs` and
  `valid75_obs` apply the minute-validity rule to observed valid windows only (the primary
  counts bridged values as valid by design of bridging, so the original valid25/valid75
  barely tested the rule). `concord` also removes valid windows where monitor MAP and the
  waveform mean differ by > 10 mmHg.
- *Pre-specified S4 and S6 had not been run.* They were omitted from `analysis.py` by error and
  are now run in `src/posthoc_stats.py` with the A15 interval.
- *Post hoc analyses* in `src/posthoc_review.py`, `src/posthoc_models.py`,
  `src/posthoc_stats.py` and `src/validate_v1_sweep.py`: discordant-patient table, TOST
  operating characteristics by simulation, split-sample interval coverage, department
  restriction, disease-risk-score adjustment, crude-to-adjusted OR ladder, real-time episode
  table, pulse oximetry during deep episodes, cuff subtype/regularity/position, rule
  performance by nadir, injection sweep.
