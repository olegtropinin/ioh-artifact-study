# Methods

## Design, data and reporting

We performed a retrospective cohort study of the open VitalDB dataset:[@vitaldb]
- 6,388 non-cardiac surgical cases;
- Seoul National University Hospital, 2016–2017;
- anaesthesia records, laboratory results, monitor numerics (GE Solar 8000) and
  high-resolution waveforms.

The institutional review board approved data collection. The data are de-identified and
public, so no further approval was needed. Reporting follows STROBE and
RECORD.[@strobe; @record]

The analysis protocol was written before any exposure–outcome association was computed and
was revised after an adversarial methods review. It was frozen by a tagged commit after the
whole analysis had run end to end on a randomly permuted outcome. The Supplementary Protocol
lists every amendment before the freeze, and every change and post hoc analysis after
unblinding, with dates and reasons. Post hoc analyses are labelled as such throughout.

A large language model (Claude, Anthropic) was used under the author's direction to write the
analysis code, to review the methods adversarially before the freeze, to simulate peer review
of the draft and to draft the text. It also served, as described below, as a secondary
blinded rater. The author checked all code, outputs and text.

## Participants

We included adults under general anaesthesia whose record contained the 500 Hz arterial
pressure waveform (radial in 95%) and at least 30 min of reference-valid monitoring. Only the
first eligible case per patient was used.

For the AKI analysis we further excluded:
- transplantation;
- patients without a baseline creatinine;
- baseline estimated glomerular filtration rate (eGFR, CKD-EPI 2021[@ckdepi]) below
  15 mL min^−1^ 1.73 m^−2^;
- patients without a creatinine measurement within 7 days after anaesthesia.

## Waveform classification and the reference series

The monitor stores systolic, diastolic and mean arterial pressure every 2 s. This is the
stream that anaesthesia information management systems store and that retrospective studies
analyse. We used the waveform only to decide *whether* each 2-s monitor value was
trustworthy, never to replace it, so calibration differences between monitor and waveform
could not enter the comparison.

Each 2-s waveform window was labelled with the first category that applied:
- *zero*: mean below 15 mmHg and 2nd–98th centile range below 10 mmHg (transducer open to
  air or being zeroed);
- *high*: maximum above 250 mmHg or mean above 200 mmHg (fast flush);
- *non-pulsatile*: range below 8 mmHg, interdecile range below 3 mmHg, or no systolic
  upstroke (a rise above 8 mmHg within 100 ms) in the centred 6-s window. This covers a
  stopcock turned off to the patient and an occluded or kinked line;
- *noise*: minimum below −10 mmHg, or median absolute second difference ≥ 4 mmHg;
- *valid*: none of the above.

Hereafter, "artefact" means a value flagged by this classifier. Because the monitor averages
over several beats, windows from 2 s before to 8 s after any
artefact run were labelled *guard*. Eight seconds was the 95th centile of the time the monitor
took to rejoin the waveform after an artefact.

Thresholds were set on outcome-free data. A pulsatility criterion based on beat-to-beat
autocorrelation was discarded before the freeze because it labelled atrial fibrillation as
artefact. Figure 1 shows examples.

**Alignment and monitoring period.**
- *Lag.* The monitor numerics lag the waveform. The lag was estimated for each case by
  maximising the correlation between monitor MAP and the waveform window mean in valid
  windows. It was 4 s in 62% of cases and 6 s in 35%.
- *Monitoring period.* It ran from the first to the last uninterrupted 60 s of valid waveform
  within anaesthesia. It began a median of 9.9 min (IQR 6.3–15.8) after the start of
  anaesthesia, so much post-induction hypotension falls outside it.[@sudfeld]

**Reference series.** The reference was the lag-aligned monitor MAP restricted to valid
windows.
- Gaps of up to 3 min, bounded on both sides by at least 30 s of valid data, were bridged by
  linear interpolation between the medians before and after the gap. Bridging avoids a
  systematic loss of true hypotension that coincides with blood sampling.
- A minute was valid if at least half of its windows were valid or bridged.

## Retrospective pipelines

A pipeline turns the monitor numbers into an exposure, using the numbers alone.

*Filters* reproduced published rules:
- F0: none;
- F1: MAP below 20 or above 250 mmHg removed;[@leesb]
- F2: MAP below 30 or above 200 mmHg removed;[@khan]
- F3: systolic above 250, diastolic below 15, MAP below 35 or above 150, or pulse pressure
  below 15 mmHg;[@jacobsson]
- F4: physiological consistency (MAP below 20 or above 200; systolic below 20 or above 300;
  systolic ≤ diastolic; pulse pressure below 5; diastolic below 5);
- F5: F4, then removal of values that differ from both neighbours by more than 30 mmHg;[@du]
- F6: F4, then a 7-point running median.[@pasma2020]

*Resolutions*:
- R1: every 2-s value;
- R2: one instantaneous value per minute;
- R3: the per-minute median;
- R4: a value charted every 5 min and held;
- R5: a value charted every 15 min and held.

R4 and R5 were evaluated at several phase offsets, and the estimates were averaged.

*Exposures*, each at thresholds of 55, 60 and 65 mmHg:
- cumulative minutes below the threshold, per 10 min, capped at 120 min;
- area under the threshold, per 100 mmHg·min, capped at the reference's 99th centile;
- time-weighted average below the threshold, in mmHg;
- the binary exposure "≥ 10 min below the threshold".

The reference was processed at every resolution in the same way. Each pipeline was compared
with the reference at the same resolution, so the contrast isolates waveform-based
cleaning. In total there were 420 pipeline specifications.

## Outcomes and covariates

The primary outcome was AKI by the KDIGO creatinine criteria:[@kdigo] an increase of
≥ 0.3 mg dL^−1^ within 48 h, or ≥ 1.5 times baseline within 7 days. Baseline was the last
creatinine within 30 days before surgery, otherwise the preoperative value.

Models were adjusted for:
- age and eGFR, as restricted cubic splines;
- sex, body mass index, ASA physical status ≥ 3 and emergency surgery;
- hypertension and diabetes;
- preoperative haemoglobin and albumin;
- department and surgical approach;
- log anaesthesia duration.

Vasopressors, fluids and blood loss were not included, because they may lie on the causal
path. With 91 events and 21 parameters there were 4.3 events per parameter. We
used Firth-penalised logistic regression with Wald intervals,[@firth] and the two models that form each ratio
share the same adjustment set.

## Statistical analysis

**Measurement error.** Each recorded minute with MAP below 65 mmHg was classed against the
reference at the same resolution:
- *spurious*: reference ≥ 65 mmHg;
- *confirmed*: reference < 65 mmHg;
- *indeterminate*: no valid reference. Indeterminate minutes were never counted as artefact.

*Masked* minutes were reference minutes below 65 mmHg that the pipeline recorded as ≥ 65 mmHg.
For the binary exposure we report κ and the number of patients whose category differed.
Proportions have patient-cluster bootstrap CIs.

**Primary estimand.** The primary estimand was the ratio of odds ratios, ROR =
OR~pipeline~ / OR~reference~, for AKI with the binary exposure "≥ 10 min below 65 mmHg". It
compared F1 × R3 with the reference at R3, using the same adjustment set and the same
patients. The ROR is largely insensitive to confounding that the two series share.

We pre-specified an equivalence margin of 0.80–1.25, the conventional margin symmetric on the
log scale:
- an interval inside the margin: equivalent;
- an interval excluding 1, with a point estimate outside the margin: material change;
- anything else: inconclusive.

Because the two exposures differ in only a few patients, the percentile bootstrap interval is
too narrow. Across 100 outcome permutations, in which the true ROR is 1, it covered 1 in only
51%. A rule written before the real outcome was examined therefore set every ROR-type
interval to:

  log ROR ± 1.96 × max(paired-bootstrap SE, SD over 200 outcome permutations).

We checked this interval by its coverage under independent permutations, and by simulating
outcomes from the adjusted reference model with differential error placed at the margin
(Supplementary Methods).

**Secondary analyses.**
- The same ROR for all 35 filter × resolution cells, with simultaneous 95% bands.
- The slope per 10 min below 65 mmHg.
- The full specification curve over metrics and thresholds.
- The effect of resolution on the reference itself.

**Differential misclassification.** We regressed AKI on log(1 + spurious minutes per monitored
hour), adjusting for:
- the reference exposure (linear and spline terms);
- log monitored hours;
- the adjustment set.

We used the raw 2-s stream (F0 × R1), because at F1 × R3 spurious minutes were non-zero in too
few patients (amendment A14, made before the freeze). The negative control was spurious
hypertensive minutes: pipeline MAP above 120 mmHg while the reference was ≤ 100 mmHg.

**Episodes.** Each run of monitor MAP below 65 mmHg was classed as:
- *waveform-flagged*: ≥ 50% of its windows labelled artefact;
- *guard-dominated*;
- *physiological*.

We tabulated the probability that an episode was flagged by final duration and nadir. The
protocol specified a depth-2 decision tree for a simple rule; the best rule was a single
split, which is reported. Post
hoc, we also tabulated it by elapsed duration and nadir so far, which is what is known while
an episode unfolds.

**Validation of the reference.**
- *Independent signals:*
  - cuff MAP within 60 s of an episode;
  - ECG and plethysmographic pulse rate during non-pulsatile windows and deep episodes;
  - the non-pulsatile fraction in atrial fibrillation.
- *Injection–recovery* of synthetic artefacts after Li et al.,[@li] with amplitude and
  duration varied post hoc. The injections resemble the classifier's own rules, so this is an
  implementation check rather than independent validation.
- *A blinded AI rating* of 152 snippets (Supplementary Methods).

**Sensitivity analyses.** The pre-specified sensitivity analyses varied:
- the reference: guard length, pulse-pressure threshold, minute validity, bridging, and the
  waveform mean in place of the monitor value;
- the monitoring period;
- the adjustment set;
- the outcome: AKI stage ≥ 2; missing postoperative creatinine counted as no AKI (S4);
  transplantation included (S6).

S4 and S6 had been omitted by error and were run after unblinding. Post hoc analyses are
listed with them in Table S5.

Analyses used Python 3.10 (NumPy, SciPy, pandas). The classifier, Firth regression, splines,
bootstrap and permutation code were written by the author and unit-tested.
