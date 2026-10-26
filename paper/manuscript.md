---
title: "Arterial-line artefacts, data resolution and the association between intraoperative hypotension and acute kidney injury: a waveform-referenced multiverse analysis"
---

**Running title:** Arterial artefacts and intraoperative hypotension research

**Author:** Oleg Tropynin

**Affiliation:** Independent researcher, Karaganda, Kazakhstan

**Correspondence:** Oleg Tropynin, tropininoleg@gmail.com

**Keywords:** intraoperative hypotension; arterial pressure; artefacts; acute kidney injury;
measurement error; multiverse analysis; VitalDB

# Abstract

**Background.** Evidence linking intraoperative hypotension to acute kidney injury (AKI) comes
from monitor numbers that include arterial-line artefacts. Whether artefact handling and data
resolution change that association, and whether artefact is recorded preferentially in
patients who develop AKI, is unknown.

**Methods.** We studied 3,249 adults in the open VitalDB dataset with a 500 Hz radial arterial
waveform. Each 2-s monitor value was labelled valid or artefact from the waveform, giving a
waveform-verified reference series. We compared it with 420 retrospective pipelines (7
published filters × 5 resolutions × 4 exposure metrics × 3 thresholds). The primary estimand
was the ratio of adjusted odds ratios (ROR) for KDIGO AKI with ≥ 10 min of mean arterial
pressure (MAP) < 65 mmHg, comparing a range filter applied to per-minute medians with the
reference, against a pre-specified equivalence margin of 0.80–1.25. Intervals were calibrated
on permuted outcomes. The protocol was frozen after an end-to-end dry run on a permuted
outcome.

**Results.** 96.3% of monitored time was artefact-free. With per-minute medians, 0.7% of
recorded hypotensive minutes were spurious, against 3.3% with one instantaneous value per
minute. A 7-point running median created 7.5% spurious minutes and masked 20% of true ones.
Of 2,563 patients in the AKI analysis, 91 (3.6%) developed AKI. The ROR was 0.96 (95% CI
0.86–1.06): equivalent. None of 35 filter × resolution combinations changed the association
significantly. Spurious hypotension was not associated with AKI and was unrelated to blood
sampling frequency. Arterial artefact was eight times more frequent in the minute before a
cuff reading. Recorded episodes below 40 mmHg lasting ≤ 60 s were artefact in 65–90%, and
episodes lasting > 1 min with a nadir ≥ 40 mmHg in ≤ 2%.

**Conclusions.** With per-minute medians and a range filter, artefacts do not bias the
association between ≥ 10 min of MAP < 65 mmHg and AKI. Running-median smoothing and
unfiltered depth-weighted metrics should be avoided. Brief, very deep falls in recorded
pressure are usually artefact. Arterial artefact clusters around cuff measurements, partly
through occlusion of the cannulated arm.

# Introduction


Intraoperative hypotension is associated with acute kidney injury, myocardial injury and
death, and thresholds derived from such studies — typically a mean arterial pressure (MAP)
below 65 mmHg for more than a few minutes — now appear in consensus statements and drive
quality metrics, trials and automated decision support.^1–3^ Almost all of this evidence
comes from retrospective analyses of numbers stored by anaesthesia information management
systems: one value per minute or less, taken from the monitor rather than from the
waveform the clinician sees.

Invasive arterial pressure is the reference standard of these studies, but the stored
numbers inherit every event that disturbs an arterial line: flushing, blood sampling,
transducer zeroing, a closed stopcock, a kinked catheter, and cuff inflation on the same
limb.^4,5^ Earlier work established three things. Choosing among published artefact
filters changes the measured incidence of hypotension up to twofold, yet changed the
association with myocardial injury little.^6^ Coarser sampling inflates the measured
burden of hypotension against a waveform reference, although its effect on outcome
associations has only been extrapolated.^7^ And how hypotension is modelled changes the
estimated odds ratios.^8^ Recent studies of the open VitalDB dataset relating
intraoperative arterial pressure to kidney injury applied a single cleaning rule or did
not describe one, and none examined its influence.^9–11^

Three questions therefore remain open. First, when artefacts are identified from the
waveform itself rather than from rules applied to the numbers, how much of recorded
hypotension is artefact? Second, does the combination of artefact rule and data resolution
change the estimated association between hypotension and acute kidney injury when that
association is estimated directly, rather than extrapolated? Third — and not, to our
knowledge, previously examined — is artefact misclassification *differential*? Arterial
blood is sampled more often in sicker and less stable patients; if sampling artefacts are
recorded as hypotension preferentially in patients who later develop kidney injury, the
error would bias published associations away from, not towards, the null.

A fourth question matters at the bedside and for automated systems: which recorded
low-pressure episodes are artefact, and can they be recognised from the numbers alone?

We used the two parallel recordings in VitalDB — the 500 Hz waveform and the monitor's 2-s
numerics — to build a waveform-referenced MAP series, and compared it with 420 pipelines
that a retrospective study could plausibly use, in a pre-specified multiverse
(specification-curve) analysis.^12,13^

# Methods


## Study design, data source and reporting

We performed a retrospective cohort study of the open VitalDB dataset, which contains
6,388 non-cardiac surgical cases at Seoul National University Hospital (2016–2017) with
anaesthesia-record data, laboratory results, monitor numerics and high-resolution
waveforms.^14^ Data collection was approved by the Seoul National University Hospital
institutional review board, and the data are de-identified and publicly released, so no new
ethics approval or consent was required for this secondary analysis. The study is reported
according to STROBE and its RECORD extension.^15,16^ The analysis protocol was written
before any exposure–outcome association was computed, was revised after an adversarial
methods review, and was frozen by a tagged commit after the complete analysis had been run
end to end on a randomly permuted outcome vector (Supplementary Protocol). Code is
available (see Data availability).

## Participants

We included adults (≥ 18 years) under general anaesthesia whose record contained the
500 Hz radial arterial pressure waveform and at least 30 min of waveform-verified
monitoring (defined below). One case per patient was retained (the first eligible case).
For the kidney analyses we further excluded transplantation, patients without a baseline
creatinine, a baseline estimated glomerular filtration rate (eGFR, CKD-EPI 2021^17^)
< 15 mL min^−1^ 1.73 m^−2^, and patients without a creatinine measurement within 7 days
after anaesthesia.

## Two views of the same arterial pressure

Each case provides two parallel recordings of the same transducer signal: the waveform
digitised at 500 Hz, and the monitor's numeric systolic, diastolic and mean arterial
pressure (MAP) every 2 s — the stream that anaesthesia information management systems
store and that retrospective studies analyse. We used the waveform only to decide *whether*
each 2-s monitor value was trustworthy, and never to replace it, so that calibration
differences between the monitor and the analogue-to-digital converter could not enter the
comparison.

**Waveform classification.** Every 2-s waveform window was labelled *valid*, *missing* (no
waveform recorded), *zero* (mean < 15 and pulse pressure < 10 mmHg: transducer open to air
or zeroing), *high* (maximum > 250 or mean > 200 mmHg: fast flush or pressure-bag
plateau), *non-pulsatile* (pulse pressure < 8 mmHg, interdecile range < 3 mmHg, or no
systolic upstroke — a rise > 8 mmHg within 100 ms — in the centred 6-s window: stopcock
closed for blood sampling, kinked or clotted line), or *noise* (minimum < −10 mmHg or median
absolute second difference ≥ 4 mmHg). Because the monitor averages over several beats,
windows from 2 s before to 8 s after any artefact run were labelled *guard* (examples in
Figure 1); the 8 s
corresponds to the 95th centile of the time the monitor took to rejoin the waveform after
an artefact. Thresholds were set on descriptive data from fewer than 600 cases, without
outcome data. A pulsatility criterion based on beat-lag autocorrelation was evaluated and
discarded before freezing because it labelled atrial fibrillation as artefact.

**Alignment and monitoring period.** Monitor values lag the waveform; the lag (2–8 s) was
estimated per case by maximising the correlation between monitor MAP and the waveform
window mean in valid windows. The monitoring period ran from the first to the last
uninterrupted 60 s of valid waveform within anaesthesia. Minutes in which the waveform was
missing for more than half the time were excluded from every series (common support);
missing waveform was not treated as artefact.

**Reference series.** The reference was the aligned monitor MAP restricted to valid windows.
Gaps of ≤ 3 min bounded on both sides by ≥ 30 s of valid data were bridged by linear
interpolation between the median MAP before and after the gap; longer gaps remained
missing. Bridging prevents a systematic loss of true hypotension that coincides with
arterial blood sampling, which would otherwise bias the reference.

## Retrospective pipelines

A pipeline is the sequence of choices a retrospective study makes to turn monitor numerics
into an exposure. Pipelines used only the monitor numerics.

*Artefact filters* reproduced published rules:
- F0: none;
- F1: MAP < 20 or > 250 mmHg removed, as in a recent VitalDB study of hypotension and
  kidney injury;^9^
- F2: MAP < 30 or > 200;^18^
- F3: systolic > 250, diastolic < 15, MAP < 35 or > 150, or pulse pressure < 15 mmHg;^7^
- F4: a physiological-consistency rule (MAP < 20 or > 200; systolic < 20 or > 300;
  systolic ≤ diastolic; pulse pressure < 5; diastolic < 5);
- F5: F4 followed by removal of values that differ from both neighbours by > 30 mmHg;^19^
- F6: F4 followed by a 7-point running median.^6^

*Resolutions*:
- R1: all 2-s values;
- R2: one instantaneous value per minute (the first available);
- R3: the per-minute median;
- R4: a value charted every 5 min and held;
- R5: a value charted every 15 min and held.

R4 and R5 were evaluated at every phase offset (R4) or at five equally spaced offsets
(R5), and estimates were averaged over offsets. F5 and F6 were applied on each pipeline's
own grid.

*Exposure metrics* were computed for thresholds of 55, 60 and 65 mmHg:
- cumulative minutes below the threshold;
- area under the threshold (mmHg·min);
- time-weighted average below the threshold;
- the binary exposure "≥ 10 cumulative minutes below the threshold".

The reference was processed at every resolution in the same way, so each pipeline was
compared with the reference at matched resolution. In total there were 420 pipeline
specifications.

## Outcomes and covariates

The primary outcome was acute kidney injury (AKI) by the creatinine criteria of KDIGO:^20^
an increase ≥ 0.3 mg dL^−1^ within 48 h, or ≥ 1.5 times baseline within 7 days.
- Baseline was the last creatinine within 30 days before induction, otherwise the
  recorded preoperative value.
- Secondary outcomes were AKI stage ≥ 2 and in-hospital death.
- Models were adjusted for:
  - age and eGFR, each as a restricted cubic spline;
  - sex, body mass index, ASA physical status ≥ 3, emergency surgery, hypertension,
    diabetes, preoperative haemoglobin and albumin, department, surgical approach, and
    log anaesthesia duration.
- Intraoperative vasopressors, fluids and blood loss were not included, as potential
  mediators.

## Statistical analysis

**Measurement error.** Each pipeline-recorded minute with MAP < 65 mmHg was classified
against the reference at the same resolution:
- *spurious*: reference ≥ 65;
- *confirmed*: reference < 65 with ≥ 50% of the minute observed;
- *bridged-low*: reference < 65 only by interpolation;
- *indeterminate*: reference missing; these minutes were never counted as artefact.

For the binary exposure we report sensitivity, specificity and Cohen's κ against the
reference. Confidence intervals for proportions use the patient-cluster bootstrap.

**Primary estimand.**
- The ratio of odds ratios, ROR = OR~pipeline~ / OR~reference~, for AKI with the binary
  exposure "≥ 10 min with MAP < 65 mmHg", comparing F1 × R3 with the reference at R3.
  At matched resolution, this contrast isolates the effect of artefact.
- Both models were Firth-penalised logistic regressions with the same adjustment set,
  fitted on the same patients.^21^
- Uncertainty came from a paired patient-level bootstrap with 2,000 resamples. Before
  unblinding, we checked the calibration of this interval on 100 independent permutations
  of the outcome, under which the true ROR is exactly 1. The percentile interval covered 1
  in only 51% of permutations for the primary contrast, because the contrast rests on the
  few patients whose exposure category differs between series and the bootstrap
  distribution is correspondingly spiky. Following a rule written down before this check
  was run, every ROR-type interval was therefore computed as log ROR ± 1.96 ×
  max(bootstrap SE, SD of log ROR over 200 outcome permutations); this interval covered 1
  in 97–100% of null permutations. Percentile intervals are reported as secondary.
- We pre-specified an equivalence margin of 0.80–1.25. A CI inside the margin means
  artefact handling does not materially change the association. A CI excluding 1 with a
  point estimate outside the margin means a material change. Anything else is
  inconclusive.
- Non-differential exposure error of plausible size moves a binary ROR only slightly
  towards 1. The ROR therefore mainly detects differential error.

**Key secondary analyses.**
- The same ROR for the raw 2-s stream (F0 × R1).
- The per-10-minute log-odds of AKI with cumulative minutes below 65 mmHg, F1 × R3 versus
  the reference, with the attenuation factor β~pipeline~/β~reference~.
- All 35 filter × resolution RORs, with simultaneous 95% bands (bootstrap max-|z| critical
  value applied to the calibrated standard error) and two-sided permutation p values.
- The full specification curve over all metrics and thresholds.
- The effect of resolution alone, as OR(reference at R) / OR(reference at R3).

**Differential misclassification.** Spurious minutes per monitored hour were correlated with
intraoperative arterial blood gases per hour and with ASA class. The analysis was
pre-specified for F1 × R3; because in the permuted dry run spurious minutes at F1 × R3 were
non-zero in only 241 patients, it was also run on the raw 2-s stream (F0 × R1; non-zero in
1,728), which is the version interpreted, with odds ratios per standard deviation of the
exposure. We then
regressed AKI on log(1 + spurious minutes per hour), adjusting for the reference
hypotension exposure (linear and spline terms), log monitored hours and the adjustment set.
- Separate models were fitted for spurious minutes dominated by zero/flush labels and by
  non-pulsatile/noise labels.
- As a negative control we used spurious *hypertensive* minutes: pipeline MAP > 120 mmHg
  while the reference was ≤ 100 mmHg. These share the same mechanism (flushing and
  sampling) but cannot hide hypotension.
- A mechanism model added blood gases per hour, blood loss and red-cell units.

**Episodes.** Contiguous runs of monitor MAP < 65 mmHg within the monitoring period were
classed as:
- *waveform-flagged*: ≥ 50% of the run's windows carry an artefact label;
- *guard-dominated*;
- *physiological*.

We tabulated the probability of being flagged by duration and nadir. A depth-≤ 2 rule using
duration, nadir and the drop from the preceding 30-s maximum was derived on a random half of
patients and validated on the other half. Leaves were called "flagged" only at ≥ 90%
specificity.

**Validation of the reference.**
- *Independent sensors*:
  - non-invasive cuff MAP within ±3 min of an episode, by episode class;
  - ECG and plethysmographic heart rate during non-pulsatile windows;
  - the non-pulsatile fraction in patients with preoperative atrial fibrillation.
- *Injection–recovery*: synthetic flush, zeroing, sampling, damping, noise and
  transducer-offset artefacts after Li et al.^22^ were inserted into clean segments.
- *A blinded rating* of 150 stratified 40-s snippets by an AI model, reported as secondary
  evidence only. A 400-snippet human adjudication set is released for future validation.

**Sensitivity analyses.**
- Guard 0 s and 30 s.
- Pulse-pressure threshold 5 and 12 mmHg.
- Reference minute validity 25% and 75%.
- Unbridged reference.
- Waveform-mean reference.
- A pipeline-specific, numerics-defined monitoring period.
- Additional adjustment for blood loss.
- Adjustment for the number of postoperative creatinine measurements.
- AKI stage ≥ 2, with a reduced adjustment set.

In-hospital mortality was analysed in one pre-specified specification with a reduced
adjustment set, because there were few deaths.

Analyses used Python 3.10 (NumPy, SciPy, pandas). Firth regression, splines, bootstrap and
the classifier were implemented by the author and unit-tested.

# Results


## Participants and data

Of 3,645 cases with an arterial waveform track, 3,434 had a retrievable waveform and 3,429 a
waveform-defined monitoring period. The descriptive cohort comprised 3,249 patients (first
case per patient; adults under general anaesthesia with ≥ 30 min of reference-valid
monitoring), contributing 11,466 h of monitoring (median 193 min per patient, IQR 134–272).
The AKI analysis set comprised 2,563 patients, of whom 91 (3.6%) developed AKI (Figure S1,
flow). Patient characteristics are shown in Table 1.

## How much of the arterial record is artefact

Within the monitoring period, 96.3% of 2-s windows were valid; 1.2% were labelled *high*
(flush or pressure-bag plateau), 0.7% *non-pulsatile*, 0.2% *noise*, 0.07% *zero*, and 1.4%
*guard*. The waveform was essentially never missing inside the monitoring period. Artefact
was ubiquitous rather than concentrated: flush events occurred in 98% of patients (2.6 per
monitored hour), non-pulsatile runs in 90% (2.0 per hour), noise in 97% (2.7 per hour) and
zeroing in 33% (0.2 per hour).

**Artefact around cuff measurements.** In 2,578 patients with both arterial and
non-invasive cuff pressure, the fraction of arterial windows labelled artefact in the 60 s
before a new cuff value was 13.9%, against 1.8% at other times (ratio 7.9; Wilcoxon
p < 10^−100^; 19,465 cuff readings). The excess peaked 16 s before the cuff value appeared,
at 25% of windows, against a baseline of 4.6% (Figure 2; 15,643 readings with a complete
−120 to +30 s window). In a post hoc comparison by cannulation site, the excess was larger
with radial catheters than with pedal or femoral catheters, which an arm cuff cannot occlude:
13.9% vs 1.8% (2,219 patients) against 9.6% vs 3.4% (58 patients; Mann–Whitney p < 0.001 for
the difference). It was also larger with right than with left radial catheters: the
proportion of patients with artefact before ≥ 10% of cuff readings was 59% vs 30%. The cuff
arm is not recorded in VitalDB.

## Spurious and masked hypotension

At the per-minute median resolution most commonly used in retrospective work (R3), 0.66%
(95% CI 0.58–0.74) of recorded minutes with MAP < 65 mmHg after the F1 filter were spurious
— the waveform-verified reference was ≥ 65 mmHg (Figure 3; Table S1). Spurious fractions were
higher with instantaneous sampling: 3.3% (3.0–3.6) with one value per minute (R2) and 2.0%
(1.9–2.2) with the raw 2-s stream (R1). The published filters F3–F5 removed most spurious
minutes at R1 and R3 (0.3–0.9%) but not at R2 (1.8–3.1%), where a single sampled value per
minute either catches an artefact or not. The 7-point running median (F6) behaved
differently from every other filter: it *created* spurious minutes (7.5% at R3, 9.9% at R2)
and masked 20% (R3) to 24% (R2) of true hypotensive minutes, because it delays and truncates
episodes.

**Binary exposure.** Against the reference at matched resolution, the binary exposure
"≥ 10 min with MAP < 65 mmHg" was classified with sensitivity ≥ 0.99, specificity
0.95–0.99 and κ 0.95–0.99 for every filter except F6 (Table S2). With F1 at R3, 38 of 3,249
patients (1.2%) changed exposure category, 32 of them upwards; 30 of the 38 flips occurred in
patients whose reference exposure lay between 5 and 10 min. Resolution changed exposure
prevalence more than any filter did: with the reference itself, 42.4% of patients were
exposed at R3 against 51.2% at R4 (5-min charting) and 53.2% at R5 (15-min charting;
both at phase offset 0). The
7-point median applied to charted data was destructive: κ 0.39 at R4 and 0.20 at R5, with
1,007 and 1,370 exposed patients reclassified as unexposed.

## Which low-pressure episodes are artefact

Of 106,725 monitor-recorded episodes of MAP < 65 mmHg in 3,123 patients, 8,471 (7.9%) were
waveform-flagged, 3,909 (3.7%) guard-dominated and 94,345 (88.4%) physiological; flagged
episodes accounted for 4.3% of hypotensive minutes. The probability that an episode was
artefact depended steeply on its depth and duration (Table 2; Figure 4):
- episodes lasting ≤ 60 s with a nadir < 40 mmHg were artefact in 65–90%;
- episodes with a nadir of 55–64 mmHg were artefact in ≤ 2.4% at every duration;
- episodes lasting > 1 min with a nadir ≥ 40 mmHg were artefact in ≤ 2%.

A single rule derived on half of the patients — a drop of more than 20 mmHg from the
maximum MAP in the preceding 30 s — identified flagged episodes in the other half with
sensitivity 0.89 (95% CI 0.85–0.91), specificity 0.92 (0.91–0.92) and positive predictive
value 0.46 (0.44–0.48).

## Validation of the reference

**Independent sensors.** Within ±3 min of a waveform-flagged episode, the cuff MAP was
≥ 70 mmHg in 83.8% (82.6–84.8) of 4,505 episodes, against 45.9% (44.9–46.8) of 10,944
physiological episodes (median cuff MAP 82 vs 69 mmHg). During 153,662 non-pulsatile
windows the ECG heart rate was 40–150 min^−1^ in 97.8% and the plethysmographic pulse rate
in 92.6%, i.e. circulation continued while the arterial trace was flat. Thirteen patients
with preoperative atrial fibrillation had a non-pulsatile fraction no higher than patients
in sinus rhythm (0.17% vs 0.68%), so the classifier did not mistake irregular rhythm for
artefact.

**Injection–recovery.** Synthetic artefacts inserted into 296 clean 2-min segments from 100
patients were detected in 100% of flush, zeroing, sampling (flat and low) and noise
injections, with no false labels outside the injected stretch and none in un-injected
segments. Over-damping was detected in 12%, and a transducer offset in none — both preserve
a pulsatile waveform and are invisible to any waveform-morphology rule.

**Blinded AI rating (secondary).** A multimodal AI model, blinded to the labels and
stratum, rated 152 stratified 40-s snippets. Excluding guard windows and 2 snippets rated
"unsure", agreement with the classifier was 97.7% (κ 0.95; n = 131): all 57 windows the
classifier called artefact were rated artefact, and 3 of 74 classifier-valid low-pressure
windows were rated artefact (noise or recovery). Of 19 guard windows, 13 were rated
artefact. Because the rater belongs to the same model family that helped design the
classifier, this is not independent validation; a 400-snippet set with a hidden key is
released for human adjudication.

## Association with acute kidney injury

**Primary estimand.** In the AKI analysis set (2,563 patients, 91 with AKI), the adjusted
odds ratio for AKI with ≥ 10 min of MAP < 65 mmHg was 0.94 with the reference series and
0.90 with the F1 × R3 pipeline. The ratio of odds ratios was 0.96 (95% CI 0.86–1.06;
permutation p = 0.42). The interval lies within the pre-specified margin of 0.80–1.25, so
artefact handling did not materially change the association: the pre-specified verdict was
*equivalent*. Firth fits failed to reach tolerance in 8 of about 182,000 bootstrap fits.

**All 35 filter × resolution cells** (Table 3; Figure 5). No cell had a 95% interval or
simultaneous band excluding 1. Twenty-five cells were equivalent and ten inconclusive. The
inconclusive cells were:
- the raw 2-s stream with F0, F1 or F2 (ROR 1.09–1.12; upper limits 1.31–1.36);
- one instantaneous value per minute with F2, F3 or F4 (upper limits 1.25–1.26);
- the 7-point median at R2–R5 (ROR 1.13–1.54, with wide intervals).

With any filter other than F6, the point estimates ranged from 0.94 to 1.12.

**Resolution alone.** Coarser resolution of the reference itself raised the proportion of
exposed patients from 42% (R3) to 51–53% (R4–R5). It did not change the odds ratio
detectably. Relative to R3, the ratio was:
- R1: 0.93 (0.80–1.08);
- R2: 1.08 (0.87–1.33);
- R4: 1.10 (0.86–1.40);
- R5: 1.04 (0.76–1.42).

**Dose.** Each 10 min of reference MAP < 65 mmHg was associated with an odds ratio for AKI
of 1.08 (0.99–1.17). With F1 × R3 the slope was 1.09; the difference in log-odds per 10 min
was 0.007 (−0.005 to 0.019).

**Exposure metric and threshold** (Figure 6; specification curve, Figure S2). Across all 420
specifications, the median ROR was 0.99 (IQR 0.95–1.01), and 91% of point estimates lay
within 0.80–1.25. Duration metrics were insensitive to processing: every minutes-based ROR
lay between 0.92 and 1.02. Depth-weighted metrics at low thresholds were not:
- With no filter (F0), the ROR at R3 was 0.30 for the time-weighted average below 55 mmHg
  and 0.60 for the area below 55 mmHg. Zero and flush values contribute very large areas
  below the threshold, which dilutes the association.
- A range filter corrected most of this. At R3, F1 gave 1.04 and 0.84, and F3 gave 1.22 and
  0.96.
- In a post hoc analysis with the same calibrated intervals, these depth effects were large
  but imprecise. Below 55 mmHg, the odds ratio per mmHg of time-weighted average fell from
  3.89 with the reference to 1.19 without a filter (ROR 0.30, 0.06–1.53; permutation
  p = 0.11). For the area below 55 mmHg the ROR was 0.60 (0.20–1.85).
- At 65 mmHg the same metrics were affected little: TWA 0.92 (0.79–1.08) and area 0.98
  (0.91–1.05) without a filter, and 1.00 (0.95–1.06) and 1.00 (0.97–1.03) with F1
  (Table S3).

In the reference series itself, the depth-weighted exposures were associated with AKI more
strongly than duration exposures. At R3 the odds ratio was 3.89 (1.65–9.19) per mmHg of
time-weighted average below 55 mmHg and 1.27 (1.00–1.60) per mmHg below 65 mmHg. For the
binary exposure "≥ 10 min below 55 mmHg" it was 1.95 (0.89–4.27).

**Sensitivity analyses** (Table S4). The primary ROR was stable when the reference was
varied:
- guard 0 or 30 s: 0.97 and 0.96;
- pulse-pressure threshold 5 or 12 mmHg: 0.96 and 0.95;
- minute validity 25% or 75%: 0.97 and 0.94;
- unbridged reference: 0.94 (0.83–1.06).

It was also stable with additional adjustment for blood loss (0.96) or for the number of
postoperative creatinine measurements (0.95), and for AKI stage ≥ 2 (24 events; 0.97). A
reference built from the waveform mean instead of the monitor value gave 0.74 (0.48–1.16),
and a pipeline-specific, numerics-defined monitoring period gave 0.91 (0.75–1.11). Both
intervals were wide and included 1.

**Differential misclassification.** Spurious hypotension was not related to how often
arterial blood was sampled (Spearman ρ with blood gases per hour 0.005, p = 0.81) and was
marginally less frequent with higher ASA class (ρ −0.06, p = 0.006). Adjusted for reference
exposure, spurious minutes on the raw stream were not associated with AKI. The odds ratio
per SD was:
- all spurious minutes: 0.93 (0.74–1.16);
- zero/flush-dominated: 1.10 (0.94–1.30);
- non-pulsatile/noise-dominated: 0.88 (0.70–1.11).

The negative control — spurious hypertensive minutes — gave 1.17 (0.96–1.43). Results at
F1 × R3 were similar but less precise (Table S5). There was therefore no evidence that
artefactual hypotension is recorded preferentially in patients who develop AKI.

**Mortality.** In the descriptive cohort without transplantation (2,962 patients, 26 deaths),
≥ 10 min of MAP < 65 mmHg had an odds ratio for in-hospital death of 1.50 (0.69–3.27) with
the reference and 1.47 (0.68–3.20) with F1 × R3 (ROR 0.98).

# Discussion


## Principal findings

In 3,249 patients with a high-resolution arterial waveform, artefacts were frequent events
but a small fraction of recorded hypotension. With the processing most retrospective studies
use — a per-minute median and a simple range filter — fewer than 1% of hypotensive minutes
were spurious, and the association between ≥ 10 min of MAP < 65 mmHg and AKI was the same
whether it was estimated from the monitor numbers or from a waveform-verified reference (ROR
0.96, 95% CI 0.86–1.06; pre-specified verdict: equivalent). No filter–resolution combination
moved the association beyond what chance allows. Artefactual hypotension was not recorded
preferentially in patients who later developed AKI, so the differential bias we set out to
test was not present.

Three choices did matter:
- **The 7-point running median.** It created and masked hypotension. On charted data it
  erased most exposure, and it produced the least stable associations.
- **Unfiltered depth-weighted exposures below 55 mmHg.** Areas and time-weighted averages
  below 55 mmHg are dominated by a few zero and flush values. The point estimates suggested
  a large dilution of the association (ROR 0.30 for the time-weighted average), though the
  post hoc interval was wide.
- **Resolution.** Charting every 5–15 min classified about a fifth more patients as exposed
  without changing the odds ratio.

At the level of individual episodes the picture differs from the cohort level. A recorded
fall below 40 mmHg lasting under a minute was artefact in most cases, whereas sustained
episodes were almost never artefact.

## Comparison with previous work

**Pasma et al.**^6^ applied eight filters to per-minute data. The filter changed the
measured incidence of hypotension up to twofold but changed the association with myocardial
injury little. Their comparison was between filters; ours was against an external
waveform-verified reference, across resolutions and exposure metrics, with an equivalence
criterion and a test for differential error. The two studies agree on duration-based
exposure and on the per-minute median, and they disagree on the 7-point median. Pasma et al.
included it among their filters. We found that it distorts exposure substantially even when
the ratio of odds ratios happens to stay near 1.

**Jacobsson et al.**^7^ showed against a waveform reference that coarse sampling
inflates measured hypotension, and they extrapolated an effect on outcome associations. We
reproduced the inflation (42% to 53% exposed) but could not detect the outcome effect. The
odds ratios with 5- and 15-min charting were within 10% of those at 1-min resolution, with
intervals that included both no effect and moderate effects.

**Cuff and arterial pressure.** Wax et al.^23^ and, recently, a preprint of a MOVER cohort
study of cuff–arterial discordance^24^ interpreted disagreement between cuff and arterial pressure
as clinical information. Our observation that arterial artefact rises eightfold in the minute
before a cuff reading identifies a measurement mechanism that generates exactly such
discordance, and is partly explained by occlusion of the cannulated arm. Studies of discordance should
exclude arterial values from the minute before each cuff reading, or show that their results
survive that exclusion.

**Artefact detection.** Earlier work compared algorithmic and machine-learning artefact
detection in anaesthesia records against human annotation.^5,25^ A recent
scoping review found no agreed reference for arterial artefact.^26^ Our classifier
uses the waveform only to decide whether a monitor value is trustworthy. This sidesteps
calibration differences between monitor and waveform and can be reproduced on any dataset
that stores both.

## A methodological lesson

The usual percentile bootstrap interval for a difference between two estimates from the same
patients was badly anti-conservative here. Under a permuted outcome it covered the true value
in only half of the trials for the primary contrast. The reason is structural: when two
exposure definitions disagree in a few dozen patients, the bootstrap distribution of their
contrast is spiky and its central 95% is too narrow. Multiverse and specification-curve
analyses routinely compare highly correlated specifications in exactly this way. Without the
null calibration, which we pre-specified only after it surfaced in the dry run, several cells
in this study would have been reported as significant differences that do not exist. We
recommend that such analyses check their intervals against permuted outcomes before
unblinding.


## Practical implications

**For investigators.**
- The per-minute median is robust. Combined with any range filter it leaves < 1% of
  hypotensive minutes spurious, and patient-level exposure categories agree with a
  waveform-verified reference at κ ≥ 0.97.
- Instantaneous per-minute sampling — the form in which many anaesthesia information
  management systems store values — carries 3–5 times more spurious hypotension, and range
  filters do not remove it.
- The 7-point running median, recommended in earlier work as a robust smoother, should not
  be used to estimate hypotension exposure. On per-minute data it creates spurious minutes
  and masks about a fifth of true hypotension. On charted 5- or 15-min data it erases
  most exposure.
- Resolution matters more than the filter: charting every 5 or 15 min raised the proportion
  of exposed patients from 42% to 51–53% against the same reference. Thresholds derived
  from charted records are therefore not transferable to high-resolution data, nor the
  reverse.

**For clinicians and automated systems.**
- A very short, very deep fall in recorded MAP is usually not hypotension. Of episodes
  lasting ≤ 60 s with a nadir < 40 mmHg, 65–90% were artefact. Episodes lasting more than a
  minute with a nadir ≥ 40 mmHg were artefact in ≤ 2%.
- A simple rule — a fall of more than 20 mmHg from the preceding 30-s maximum — identified
  nine of ten artefactual episodes while falsely flagging about one physiological episode in
  twelve. Its positive predictive value (0.46) is too low for it to suppress an alarm
  silently. It is better used to prompt a glance at the waveform before treating, and to
  clean data retrospectively.
- Cuff cycling is a frequent and probably avoidable source of arterial artefact. Artefact on
  the arterial trace was eight times more frequent in the minute before a cuff value
  appeared than at other times. It peaked 16 s before the value, during the inflation and
  measurement cycle.
  - It was stronger with radial than with pedal or femoral catheters, and stronger on the
    right than on the left. This pattern fits occlusion of the cannulated arm in a subset
    of patients.
  - The excess with lower-limb catheters shows that this is not the whole explanation;
    other activity that coincides with cuff cycles, such as handling of the arm or the
    line, probably contributes.

  Placing the cuff on the arm opposite the arterial line, or suspending cuff cycling while
  the line is working, is a simple measure that a prospective study could test. In retrospective studies that compare cuff and arterial pressure (for example
  studies of cuff–arterial discordance), arterial values from the minute before each cuff
  reading are enriched for artefact and should be treated with caution.

## Strengths

- To our knowledge, the first waveform-referenced multiverse analysis of intraoperative
  hypotension and AKI: every pipeline compared with a reference at matched resolution,
  rather than with another pipeline.
- The reference never replaces monitor values, so calibration differences between the
  monitor and the analogue-to-digital converter do not enter the comparison.
- Independent physiological checks of the reference (cuff pressure, ECG and
  plethysmographic pulse, atrial fibrillation), injection–recovery, and a pre-specified
  null calibration of the inferential method.
- Analysis protocol frozen after an end-to-end dry run on a permuted outcome. Every
  deviation from it is recorded with its reason and timing.
- All data are public and all code is released.

## Limitations

- **No human adjudication.** No human expert rated the reference. Its validity rests on
  physiological cross-checks, injection–recovery and an AI rater from the same model family
  that helped design the classifier, which is not independent. A 400-snippet adjudication
  set with a hidden key is released so that this gap can be closed by others.
- **Blind spots of morphology rules.** Over-damping was detected in only 12% of injections
  and a transducer offset not at all. Both preserve a pulsatile trace, so any
  morphology-based reference, ours included, will miss them. Over-damping lowers systolic
  but changes MAP little, which limits the consequence for MAP-based exposure.
- **Single centre.** One centre (Seoul National University Hospital, 2016–2017), mainly
  general and thoracic surgery, with few deaths and a low incidence of creatinine-defined
  AKI (3.6%). Precision for the AKI association itself is modest. Our contrast is a ratio
  of two estimates from the same patients, which is much more precise than either
  estimate.
- **Generalisability of artefact frequency.** Practice determines artefact frequency:
  sampling frequency, flushing, cuff placement and zeroing all vary by institution. The
  absolute figures will not transfer, but the mechanisms and the direction of the
  resolution and smoothing effects should.
- **Creatinine-only AKI.** AKI was defined by creatinine only, without urine output, and
  ascertainment depended on postoperative creatinine sampling. This was addressed in a
  sensitivity analysis but not eliminated.
- **Thresholds and outcome scope.** Thresholds were tuned on descriptive data before
  outcomes were examined. Two amendments (A14, A15) were made after the permuted dry run
  but before unblinding.

## Conclusions

Arterial-line artefacts are frequent events but a small part of recorded hypotension. With
per-minute medians and a simple range filter, they do not bias the association between
≥ 10 min of MAP < 65 mmHg and AKI, and they are not recorded preferentially in patients who
develop AKI. Investigators should avoid running-median smoothing and unfiltered
depth-weighted exposures, and should report resolution as carefully as thresholds.
Clinicians and automated systems should treat a brief, very deep fall in recorded pressure as
probable artefact until the waveform says otherwise. The cuff should be placed on the
arm opposite an arterial line where possible.

# Declarations

**Ethics.** This is a secondary analysis of the de-identified, publicly released VitalDB
dataset. Collection of the data was approved by the institutional review board of Seoul
National University Hospital, as described in the data descriptor.^14^ No further
approval or consent was required.

**Funding.** None.

**Competing interests.** None declared.

**Data and code availability.** VitalDB is openly available at https://vitaldb.net. The
analysis code, the frozen protocol with all amendments, the permuted dry run, aggregate
results and the 400-snippet adjudication set are available at [REPOSITORY URL]. The
adjudication key is available from the author on request, to preserve blinding of future
raters.

**Use of artificial intelligence.** The author used an AI system (Claude, Anthropic) for
substantial parts of this work, under the author's direction:
- writing the analysis code;
- an adversarial review of the methods before the protocol was frozen;
- drafting the manuscript.

An instance of the same AI system was also used as the blinded secondary rater of waveform
snippets, as described in the Methods. The author checked the code, outputs and text, and
takes full responsibility for the content. The AI system is not an author.

**Author contribution.** O.T. conceived and designed the study, performed the analysis,
interpreted the results and wrote the manuscript.

**Acknowledgements.** The author thanks the VitalDB team at Seoul National University
Hospital for making the dataset openly available.

# Figure legends

**Figure 1.** Examples of recorded hypotension that is artefact. Each panel shows the 500 Hz
arterial waveform (grey) and the lag-aligned 2-s monitor MAP (orange) around the start of a
recorded MAP < 65 mmHg (time 0). Shaded windows are labelled artefact or guard by the
classifier. The panels show, from top to bottom:
- transducer open to air (zeroing);
- closed stopcock during blood sampling;
- fast flush followed by recovery;
- a non-pulsatile trace with a cuff reading within 3 min.

**Figure 2.** Arterial artefact around non-invasive cuff measurements. The percentage of 2-s
arterial windows labelled artefact is plotted against time relative to the moment a new cuff
value appears (15,643 readings with a complete window).

**Figure 3.** Spurious minutes among recorded minutes with MAP < 65 mmHg, by filter
(F0–F6) and resolution (2-s, one value per minute, 1-min median). Orange bars show spurious
minutes (reference ≥ 65 mmHg), with patient-cluster bootstrap 95% CIs. Blue bars show
indeterminate minutes (no valid reference), which were never counted as artefact.

**Figure 4.** Probability that a recorded episode of MAP < 65 mmHg is waveform-flagged
artefact, by episode duration and nadir (106,725 episodes in 3,123 patients).

**Figure 5.** Ratio of odds ratios for AKI (≥ 10 min MAP < 65 mmHg) for every filter ×
resolution combination, each against the reference at the same resolution. Thin lines show
95% CIs (log ROR ± 1.96 × max(bootstrap SE, permutation-null SD)). Wide bands show
simultaneous 95% bands over the 35 cells. Grey shows the equivalence margin of 0.80–1.25.

**Figure 6.** Ratio of odds ratios at the 1-min median resolution by filter, exposure metric
and threshold. Orange cells: ROR < 1; blue cells: ROR > 1. AUC, area under the threshold; TWA, time-weighted average below the
threshold.

**Figure S1.** Flow of patients (see Results for counts).

**Figure S2.** Specification curve: ratios of odds ratios for all 420 pipeline
specifications, sorted. The lower panel marks the filter, resolution and threshold of each.

# References

1. Walsh M, Devereaux PJ, Garg AX, Kurz A, Turan A, Rodseth RN, et al. Relationship between intraoperative mean arterial pressure and clinical outcomes after noncardiac surgery: toward an empirical definition of hypotension. Anesthesiology. 2013;119(3):507-15. doi:10.1097/ALN.0b013e3182a10e26
2. Salmasi V, Maheshwari K, Yang D, Mascha EJ, Singh A, Sessler DI, et al. Relationship between intraoperative hypotension, defined by either reduction from baseline or absolute thresholds, and acute kidney and myocardial injury after noncardiac surgery. Anesthesiology. 2017;126(1):47-65. doi:10.1097/ALN.0000000000001432
3. Sessler DI, Bloomstone JA, Aronson S, Berry C, Gan TJ, Kellum JA, et al. Perioperative Quality Initiative consensus statement on intraoperative blood pressure, risk and outcomes for elective surgery. Br J Anaesth. 2019;122(5):563-74. doi:10.1016/j.bja.2019.01.013
4. Kool NP, van Waes JAR, Bijker JB, Peelen LM, van Wolfswinkel L, de Graaff JC, et al. Artifacts in research data obtained from an anesthesia information and management system. Can J Anaesth. 2012;59(9):833-41. doi:10.1007/s12630-012-9754-0
5. Pasma W, Wesselink EM, van Buuren S, de Graaff JC, van Klei WA. Artifacts annotations in anesthesia blood pressure data by man and machine. J Clin Monit Comput. 2021;35(2):259-67. doi:10.1007/s10877-020-00574-z
6. Pasma W, Peelen LM, van Buuren S, van Klei WA, de Graaff JC. Artifact processing methods influence on intraoperative hypotension quantification and outcome effect estimates. Anesthesiology. 2020;132(4):723-37. doi:10.1097/ALN.0000000000003131
7. Jacobsson M, Valadkhani A, Winski G, Bell M. Accuracy of quantifying hypotension during surgery using physiological sensor data. IEEE J Transl Eng Health Med. 2026;14:265-73. doi:10.1109/JTEHM.2026.3698197
8. Vernooij LM, van Klei WA, Machina M, Pasma W, Beattie WS, Peelen LM. Different methods of modelling intraoperative hypotension and their association with postoperative complications in patients undergoing non-cardiac surgery. Br J Anaesth. 2018;120(5):1080-9. doi:10.1016/j.bja.2018.01.033
9. Lee SB. Causal effect and personalization of intraoperative hypotension burden on postoperative acute kidney injury: a doubly robust analysis of the VitalDB cohort. J Pers Med. 2026;16(7):371. doi:10.3390/jpm16070371
10. Ensarioğlu M, Yıldırım AK. Intraoperative arterial waveform morphology trajectories and prediction of postoperative acute kidney injury: a latent-class analysis of the VitalDB registry. J Clin Med. 2026;15(17):6871. doi:10.3390/jcm15176871
11. Folks R, Tsang S, Brown DE, Blanks ZD, Moradinasab N, Mazzeffi M, et al. Intraoperative short-term blood pressure variability and postoperative acute kidney injury: a single-center retrospective cohort study using sample entropy analysis. BMC Anesthesiol. 2024;24(1):395. doi:10.1186/s12871-024-02784-3
12. Steegen S, Tuerlinckx F, Gelman A, Vanpaemel W. Increasing transparency through a multiverse analysis. Perspect Psychol Sci. 2016;11(5):702-12. doi:10.1177/1745691616658637
13. Simonsohn U, Simmons JP, Nelson LD. Specification curve analysis. Nat Hum Behav. 2020;4(11):1208-14. doi:10.1038/s41562-020-0912-z
14. Lee HC, Park Y, Yoon SB, Yang SM, Park D, Jung CW. VitalDB, a high-fidelity multi-parameter vital signs database in surgical patients. Sci Data. 2022;9(1):279. doi:10.1038/s41597-022-01411-5
15. von Elm E, Altman DG, Egger M, Pocock SJ, Gøtzsche PC, Vandenbroucke JP. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement: guidelines for reporting observational studies. Lancet. 2007;370(9596):1453-7. doi:10.1016/S0140-6736(07)61602-X
16. Benchimol EI, Smeeth L, Guttmann A, Harron K, Moher D, Petersen I, et al. The REporting of studies Conducted using Observational Routinely-collected health Data (RECORD) statement. PLoS Med. 2015;12(10):e1001885. doi:10.1371/journal.pmed.1001885
17. Inker LA, Eneanya ND, Coresh J, Tighiouart H, Wang D, Sang Y, et al. New creatinine- and cystatin C-based equations to estimate GFR without race. N Engl J Med. 2021;385(19):1737-49. doi:10.1056/NEJMoa2102953
18. Khan JM, Maslove DM, Boyd JG. Optimized arterial line artifact identification algorithm cleans high-frequency arterial line data with high accuracy in critically ill patients. Crit Care Explor. 2022;4(12):e0814. doi:10.1097/CCE.0000000000000814
19. Du CH, Glick D, Tung A. Error-checking intraoperative arterial line blood pressures. J Clin Monit Comput. 2019;33(3):407-12. doi:10.1007/s10877-018-0167-7
20. Kidney Disease: Improving Global Outcomes (KDIGO) Acute Kidney Injury Work Group. KDIGO clinical practice guideline for acute kidney injury. Kidney Int Suppl. 2012;2(1):1-138.
21. Firth D. Bias reduction of maximum likelihood estimates. Biometrika. 1993;80(1):27-38. doi:10.1093/biomet/80.1.27
22. Li Q, Mark RG, Clifford GD. Artificial arterial blood pressure artifact models and an evaluation of a robust blood pressure and heart rate estimator. Biomed Eng Online. 2009;8:13. doi:10.1186/1475-925X-8-13
23. Wax DB, Lin HM, Leibowitz AB. Invasive and concomitant noninvasive intraoperative blood pressure monitoring: observed differences in measurements and associated therapeutic interventions. Anesthesiology. 2011;115(5):973-8. doi:10.1097/ALN.0b013e3182330286
24. Liu Z, Zhuang Z, Wang S, Xu X, Wu E, Ma F, et al. Intraoperative cuff–arterial pressure discordance and postoperative creatinine doubling: a retrospective MOVER cohort study [Preprint]. Research Square. 2026. doi:10.21203/rs.3.rs-11148992/v1
25. Maleczek M, Laxar D, Kapral L, Kuhrn M, Abulesz YT, Dibiasi C, et al. A comparison of five algorithmic methods and machine learning pattern recognition for artifact detection in electronic records of five different vital signs: a retrospective analysis. Anesthesiology. 2024;141(1):32-43. doi:10.1097/ALN.0000000000004971
26. Bergmann T, Vakitbilir N, Nemoga-Stout X, Sainbhi AS, Stein KY, Silvaggio N, et al. Artifact management methodologies for arterial blood pressure signals: a systematic scoping review of human and animal literature. Physiol Rep. 2025;13(19):e70533. doi:10.14814/phy2.70533

## Table 1. Patient characteristics

| Characteristic | Descriptive cohort | AKI set: no AKI | AKI set: AKI |
|---|---|---|---|
| n | 3249 | 2472 | 91 |
| Age, years | 61 (51–69) | 62 (54–70) | 63 (56–72) |
| Female | 1444 (44.4) | 1053 (42.6) | 19 (20.9) |
| BMI, kg m⁻² | 23.0 (20.8–25.2) | 23.1 (20.9–25.2) | 22.6 (20.4–26.0) |
| ASA physical status ≥ 3 | 492 (15.1) | 283 (11.4) | 28 (30.8) |
| Emergency surgery | 413 (12.7) | 266 (10.8) | 19 (20.9) |
| Hypertension | 1085 (33.4) | 835 (33.8) | 42 (46.2) |
| Diabetes | 398 (12.2) | 318 (12.9) | 18 (19.8) |
| Baseline eGFR, mL min⁻¹ 1.73 m⁻² | 95 (82–104) | 95 (83–103) | 94 (74–104) |
| Preoperative haemoglobin, g dL⁻¹ | 13.0 (11.6–14.2) | 13.1 (11.8–14.3) | 11.7 (10.4–13.6) |
| General surgery | 2017 (62.1) | 1430 (57.8) | 67 (73.6) |
| Thoracic surgery | 1001 (30.8) | 943 (38.1) | 17 (18.7) |
| Gynaecology / urology | 231 (7.1) | 99 (4.0) | 7 (7.7) |
| Open approach | 1318 (40.6) | 908 (36.7) | 61 (67.0) |
| Anaesthesia duration, h | 3.8 (2.8–5.2) | 3.8 (2.8–4.9) | 4.3 (3.2–6.3) |
| Monitored time, min | 193 (134–272) | 188 (135–258) | 223 (157–346) |
| Reference minutes MAP < 65 mmHg | 7 (1–19) | 7 (1–18) | 11 (4–39) |
| Reference ≥ 10 min MAP < 65 mmHg | 1377 (42.4) | 1021 (41.3) | 49 (53.8) |

Values are median (IQR) or n (%). Reference = waveform-verified monitor MAP, 1-min median.

## Table 2. Probability that a recorded low-MAP episode is waveform-flagged artefact

| Nadir \ duration | <=10 s | 11-30 s | 31-60 s | 1-2 min | 2-5 min | >5 min |
|---|---|---|---|---|---|---|
| <20 mmHg | 79% (77–81); n = 1569 | 77% (74–80); n = 905 | 65% (58–71); n = 201 | 43% (34–52); n = 122 | 23% (16–31); n = 150 | 11% (4–21); n = 116 |
| 20-39 mmHg | 67% (64–70); n = 755 | 90% (89–92); n = 1813 | 75% (70–80); n = 386 | 12% (6–18); n = 125 | 1% (0–3); n = 232 | 4% (1–6); n = 248 |
| 40-54 mmHg | 59% (56–63); n = 1391 | 65% (61–69); n = 1508 | 13% (10–16); n = 661 | 2% (1–4); n = 903 | 1% (0–1); n = 1578 | 1% (0–2); n = 1177 |
| 55-64 mmHg | 2% (2–3); n = 66981 | 1% (1–2); n = 13525 | 1% (0–2); n = 5286 | 1% (0–2); n = 3346 | 0% (0–1); n = 2867 | 1% (0–1); n = 880 |

Episode: contiguous run of monitor MAP < 65 mmHg. Percent flagged (patient-cluster bootstrap 95% CI); n = episodes.

## Table 3. Every filter × resolution: measurement error and its effect on the AKI association

| Filter | Resolution | Spurious % of low minutes | Masked % | Exposed, pipeline / reference % | κ | ROR (95% CI) | Simultaneous band |
|---|---|---|---|---|---|---|---|
| F0 none | 2-s stream | 2.3 | 1.0 | 44.1 / 42.3 | 0.96 | 1.12 (0.92–1.36) | 0.82–1.54 |
| F0 none | 1 value/min | 3.4 | 1.8 | 46.5 / 44.5 | 0.95 | 1.06 (0.89–1.25) | 0.80–1.39 |
| F0 none | 1-min median | 0.8 | 1.3 | 43.4 / 42.4 | 0.97 | 0.99 (0.88–1.11) | 0.82–1.20 |
| F0 none | 5-min chart | – | – | 53.1 / 51.2 | 0.95 | 0.94 (0.86–1.04) | 0.81–1.10 |
| F0 none | 15-min chart | – | – | 54.4 / 53.2 | 0.96 | 0.99 (0.92–1.07) | 0.87–1.12 |
| F1 MAP 20–250 | 2-s stream | 2.0 | 0.8 | 43.7 / 42.3 | 0.96 | 1.09 (0.91–1.31) | 0.81–1.47 |
| F1 MAP 20–250 | 1 value/min | 3.3 | 1.8 | 46.3 / 44.5 | 0.96 | 1.06 (0.89–1.25) | 0.80–1.39 |
| F1 MAP 20–250 | 1-min median | 0.7 | 1.1 | 43.2 / 42.4 | 0.98 | 0.96 (0.86–1.06) | 0.80–1.14 |
| F1 MAP 20–250 | 5-min chart | – | – | 52.9 / 51.2 | 0.95 | 0.95 (0.87–1.03) | 0.82–1.09 |
| F1 MAP 20–250 | 15-min chart | – | – | 54.2 / 53.2 | 0.97 | 1.00 (0.93–1.08) | 0.88–1.13 |
| F2 MAP 30–200 | 2-s stream | 1.8 | 0.6 | 43.5 / 42.3 | 0.97 | 1.12 (0.94–1.34) | 0.83–1.50 |
| F2 MAP 30–200 | 1 value/min | 3.3 | 1.7 | 46.3 / 44.5 | 0.96 | 1.06 (0.90–1.25) | 0.81–1.39 |
| F2 MAP 30–200 | 1-min median | 0.5 | 0.9 | 43.0 / 42.4 | 0.98 | 0.97 (0.87–1.08) | 0.82–1.15 |
| F2 MAP 30–200 | 5-min chart | – | – | 53.0 / 51.2 | 0.95 | 0.94 (0.87–1.02) | 0.82–1.08 |
| F2 MAP 30–200 | 15-min chart | – | – | 54.3 / 53.2 | 0.97 | 1.01 (0.93–1.08) | 0.89–1.13 |
| F3 Jacobsson | 2-s stream | 0.6 | 0.4 | 42.5 / 42.3 | 0.98 | 1.05 (0.93–1.19) | 0.86–1.28 |
| F3 Jacobsson | 1 value/min | 3.1 | 1.6 | 46.1 / 44.5 | 0.96 | 1.07 (0.91–1.26) | 0.81–1.40 |
| F3 Jacobsson | 1-min median | 0.3 | 0.8 | 42.9 / 42.4 | 0.98 | 0.98 (0.89–1.08) | 0.83–1.15 |
| F3 Jacobsson | 5-min chart | – | – | 53.1 / 51.2 | 0.95 | 0.95 (0.88–1.03) | 0.83–1.08 |
| F3 Jacobsson | 15-min chart | – | – | 54.3 / 53.2 | 0.97 | 1.01 (0.94–1.09) | 0.90–1.14 |
| F4 consistency | 2-s stream | 0.9 | 0.6 | 42.8 / 42.3 | 0.98 | 1.03 (0.91–1.16) | 0.84–1.26 |
| F4 consistency | 1 value/min | 3.3 | 1.7 | 46.4 / 44.5 | 0.96 | 1.06 (0.89–1.25) | 0.80–1.39 |
| F4 consistency | 1-min median | 0.4 | 0.9 | 42.9 / 42.4 | 0.98 | 0.97 (0.88–1.07) | 0.82–1.14 |
| F4 consistency | 5-min chart | – | – | 53.3 / 51.2 | 0.95 | 0.94 (0.86–1.02) | 0.82–1.08 |
| F4 consistency | 15-min chart | – | – | 54.4 / 53.2 | 0.97 | 1.00 (0.93–1.08) | 0.89–1.13 |
| F5 F4 + neighbour | 2-s stream | 0.9 | 0.6 | 42.8 / 42.3 | 0.98 | 1.03 (0.91–1.16) | 0.84–1.26 |
| F5 F4 + neighbour | 1 value/min | 1.8 | 0.8 | 45.5 / 44.5 | 0.97 | 1.00 (0.83–1.20) | 0.74–1.34 |
| F5 F4 + neighbour | 1-min median | 0.3 | 0.7 | 42.8 / 42.4 | 0.98 | 0.97 (0.88–1.07) | 0.82–1.14 |
| F5 F4 + neighbour | 5-min chart | – | – | 51.8 / 51.2 | 0.96 | 0.95 (0.87–1.03) | 0.82–1.09 |
| F5 F4 + neighbour | 15-min chart | – | – | 52.1 / 53.2 | 0.95 | 1.03 (0.95–1.12) | 0.90–1.19 |
| F6 F4 + 7-pt median | 2-s stream | 3.0 | 3.5 | 42.4 / 42.3 | 0.98 | 0.99 (0.89–1.09) | 0.84–1.17 |
| F6 F4 + 7-pt median | 1 value/min | 9.9 | 24.0 | 36.1 / 44.5 | 0.82 | 1.13 (0.83–1.54) | 0.68–1.88 |
| F6 F4 + 7-pt median | 1-min median | 7.5 | 19.9 | 36.2 / 42.4 | 0.86 | 1.22 (0.92–1.61) | 0.77–1.92 |
| F6 F4 + 7-pt median | 5-min chart | – | – | 20.3 / 51.2 | 0.39 | 1.54 (0.97–2.44) | 0.72–3.28 |
| F6 F4 + 7-pt median | 15-min chart | – | – | 11.0 / 53.2 | 0.20 | 1.18 (0.67–2.07) | 0.46–2.99 |

Spurious: pipeline minute < 65 mmHg with reference ≥ 65. Masked: share of reference minutes < 65 that the pipeline records ≥ 65; neither is defined for charted resolutions. Exposure: ≥ 10 min with MAP < 65 mmHg; exposure prevalence and κ from the descriptive cohort (charted resolutions at phase offset 0). ROR (ratio of odds ratios, pipeline / reference at matched resolution) from the AKI set; 95% CI = log ROR ± 1.96 × max(paired-bootstrap SE, permutation-null SD); simultaneous band: bootstrap max-|z| critical value over all 35 cells applied to the same SE.
