# Methods

## Design, data and reporting

We performed a retrospective cohort study of the open VitalDB dataset: 6,388 non-cardiac
surgical cases at Seoul National University Hospital in 2016–2017, with anaesthesia records,
laboratory results, monitor numerics (GE Solar 8000) and high-resolution waveforms.[@vitaldb]
Reporting follows STROBE and RECORD.[@strobe; @record]

The analysis protocol was written before any exposure–outcome association was computed,
revised after an adversarial methods review, and frozen by a tagged commit after the whole
analysis had run end to end on a randomly permuted outcome. The protocol in Online
Resource 1 lists every amendment before the freeze, and every change and post hoc analysis
after unblinding, with dates and reasons. Post hoc analyses are labelled as such throughout.

A large language model (Claude Opus 5.5, Anthropic) was used under the author's direction to
write the analysis code, review the methods adversarially before the freeze, simulate peer
review and draft the text, and as a secondary blinded rater. The author checked all code,
outputs and text.

## Participants

We included adults under general anaesthesia whose record contained the 500 Hz arterial
pressure waveform (radial in 95%) and at least 30 min of reference-valid monitoring, using the
first eligible case per patient. For the AKI analysis we further excluded transplantation and
patients without a baseline creatinine, with a baseline estimated glomerular filtration rate
(eGFR, CKD-EPI 2021[@ckdepi]) below 15 mL min^−1^ 1.73 m^−2^, or without a creatinine
measurement within 7 days after anaesthesia.

## Waveform classification and the reference series

The monitor stores arterial pressures every 2 s; this is the stream that anaesthesia
information systems store and retrospective studies analyse. We used the waveform only to
decide *whether* each 2-s monitor value was trustworthy, never to replace it, so calibration
differences between monitor and waveform could not enter the comparison.

Each 2-s waveform window was labelled *zero* (mean below 15 mmHg with a range below 10 mmHg:
transducer open to air), *high* (maximum above 250 or mean above 200 mmHg: fast flush),
*non-pulsatile* (range below 8 mmHg, interdecile range below 3 mmHg, or no systolic upstroke in
the centred 6-s window: stopcock off to the patient or occluded line), *noise* (minimum below
−10 mmHg or a large median second difference) or otherwise *valid* (Online Resource 1).

Hereafter, "artefact" means a value flagged by this classifier. Because the monitor averages
over several beats, windows from 2 s before to 8 s after any artefact run were labelled
*guard*; 8 s was the 95th centile of the time the monitor took to rejoin the waveform.
Thresholds were set on outcome-free data. A beat-to-beat autocorrelation criterion was
discarded before the freeze because it labelled atrial fibrillation as artefact. Fig. 1
shows examples.

Monitor numerics lag the waveform; the lag was estimated per case by maximising the
correlation between monitor MAP and the waveform window mean (4 s in 62% of cases, 6 s in
35%). The monitoring period ran from the first to the last uninterrupted 60 s of valid
waveform within anaesthesia. It began a median of 9.9 min (IQR 6.3–15.8) after the start of
anaesthesia, so much post-induction hypotension falls outside it.[@sudfeld]

The reference was the lag-aligned monitor MAP restricted to valid windows. Gaps of up to
3 min, bounded on both sides by at least 30 s of valid data, were bridged linearly between the
medians before and after, which avoids a systematic loss of true hypotension that coincides
with blood sampling. A minute was valid if at least half of its windows were valid or bridged.

## Retrospective pipelines

A pipeline turns the monitor numbers into an exposure, using the numbers alone. Seven
*filters* reproduced published rules: none (F0); range filters on MAP of 20–250 mmHg
(F1)[@leesb] and 30–200 mmHg (F2);[@khan] a multi-signal rule (F3);[@jacobsson] a
physiological-consistency rule (F4); F4 with removal of values differing from both neighbours
by more than 30 mmHg (F5);[@du] and F4 with a 7-point running median (F6).[@pasma2020] Full
definitions are in Online Resource 1. Five *resolutions* were every 2-s value (R1), one
instantaneous value per minute (R2), the per-minute median (R3), and a value charted every
5 min (R4) or 15 min (R5) and held; R4 and R5 were averaged over phase offsets.

*Exposures* at thresholds of 55, 60 and 65 mmHg were cumulative minutes below the threshold
(per 10 min, capped at 120 min), area under the threshold (per 100 mmHg·min, capped at the
reference's 99th centile), time-weighted average below the threshold (per mmHg) and the binary
"≥ 10 min below the threshold". Each of the 420 pipeline specifications was compared with the
reference processed the same way at the same resolution, so the contrast isolates
waveform-based cleaning.

## Outcomes and covariates

The primary outcome was AKI by the KDIGO creatinine criteria:[@kdigo] an increase of
≥ 0.3 mg dL^−1^ within 48 h, or ≥ 1.5 times baseline within 7 days. Baseline was the last
creatinine within 30 days before surgery, otherwise the preoperative value.

Models were adjusted for age and eGFR (restricted cubic splines), sex, body mass index, ASA
physical status ≥ 3, emergency surgery, hypertension, diabetes, preoperative haemoglobin and
albumin, department, surgical approach and log anaesthesia duration. Vasopressors, fluids and
blood loss were not included, because they may lie on the causal path. With 91 events and 21
parameters there were 4.3 events per parameter. We used Firth-penalised logistic regression
with Wald intervals,[@firth] and the two models that form each ratio share the same
adjustment set.

## Statistical analysis

**Measurement error.** Each recorded minute with MAP below 65 mmHg was classed against the
reference at the same resolution as *spurious* (reference ≥ 65 mmHg), *confirmed* (reference
< 65 mmHg) or *indeterminate* (no valid reference; never counted as artefact). *Masked*
minutes were the converse. For the binary exposure we report κ and the number of patients whose
category differed; proportions have patient-cluster bootstrap CIs.

**Primary estimand.** The primary estimand was the ratio of odds ratios, ROR =
OR~pipeline~ / OR~reference~, for AKI with the binary exposure "≥ 10 min below 65 mmHg". It
compared F1 × R3 with the reference at R3, using the same adjustment set and the same
patients, so it is largely insensitive to confounding that the two series share. We
pre-specified an equivalence margin of 0.80–1.25, the conventional margin symmetric on the log
scale: an interval inside the margin meant equivalent; an interval excluding 1 with a point
estimate outside the margin meant material change; anything else was inconclusive.

Because the two exposures differ in only a few patients, the percentile bootstrap interval
covered the true ROR of 1 in only 51% of 100 outcome permutations. A rule written before the
real outcome was examined therefore set every ROR-type interval to:

  log ROR ± 1.96 × max(paired-bootstrap SE, SD over 200 outcome permutations).

We checked this interval by its coverage under independent permutations and by simulating
outcomes from the adjusted reference model with differential error placed at the margin
(Online Resource 1).

**Secondary analyses** were the ROR for all 35 filter × resolution cells with simultaneous 95%
bands, the slope per 10 min below 65 mmHg, the specification curve and the effect of
resolution on the reference itself.

**Differential misclassification.** We regressed AKI on log(1 + spurious minutes per
monitored hour), adjusting for the reference exposure (linear and spline terms), log monitored
hours and the adjustment set. We used the raw 2-s stream (F0 × R1), because at F1 × R3
spurious minutes were non-zero in too few patients (amendment A14, before the freeze). The
negative control was spurious hypertensive minutes: pipeline MAP above 120 mmHg while the
reference was ≤ 100 mmHg.

**Episodes.** Each run of monitor MAP below 65 mmHg was classed as *waveform-flagged* (≥ 50% of
its windows labelled artefact), *guard-dominated* or *physiological*, and the probability of
being flagged was tabulated by final duration and nadir; a pre-specified depth-2 tree searched
for a simple rule. Post hoc, we also tabulated it by elapsed duration and nadir so far.

**Validation of the reference.** We compared flagged and physiological episodes against
independent signals (cuff MAP, ECG and plethysmographic pulse rate). Injection–recovery of
synthetic artefacts after Li et al.[@li] checked the implementation only, and a blinded AI
rater scored 152 snippets (Online Resource 1).

**Sensitivity analyses.** Pre-specified sensitivity analyses varied the reference
definition, the monitoring period, the adjustment set and the outcome (Online Resource 1). Two
of them, S4 and S6, had been omitted by error and were run after unblinding.

Analyses used Python 3.10 (NumPy, SciPy, pandas), with study code that was unit-tested.
