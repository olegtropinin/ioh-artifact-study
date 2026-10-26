# Methods

## Study design, data source and reporting

We performed a retrospective cohort study of the open VitalDB dataset, which contains
6,388 non-cardiac surgical cases at Seoul National University Hospital (2016–2017) with
anaesthesia-record data, laboratory results, monitor numerics and high-resolution
waveforms.^1^ Data collection was approved by the Seoul National University Hospital
institutional review board, and the data are de-identified and publicly released, so no new
ethics approval or consent was required for this secondary analysis. The study is reported
according to STROBE and its RECORD extension.^2,3^ The analysis protocol was written
before any exposure–outcome association was computed, was revised after an adversarial
methods review, and was frozen by a tagged commit after the complete analysis had been run
end to end on a randomly permuted outcome vector (Supplementary Protocol). Code is
available (see Data availability).

## Participants

We included adults (≥ 18 years) under general anaesthesia whose record contained the
500 Hz radial arterial pressure waveform and at least 30 min of waveform-verified
monitoring (defined below). One case per patient was retained (the first eligible case).
For the kidney analyses we further excluded transplantation, patients without a baseline
creatinine, a baseline estimated glomerular filtration rate (eGFR, CKD-EPI 2021^4^)
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
windows from 2 s before to 8 s after any artefact run were labelled *guard*; the 8 s
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
  kidney injury;^5^
- F2: MAP < 30 or > 200;^6^
- F3: systolic > 250, diastolic < 15, MAP < 35 or > 150, or pulse pressure < 15 mmHg;^7^
- F4: a physiological-consistency rule (MAP < 20 or > 200; systolic < 20 or > 300;
  systolic ≤ diastolic; pulse pressure < 5; diastolic < 5);
- F5: F4 followed by removal of values that differ from both neighbours by > 30 mmHg;^8^
- F6: F4 followed by a 7-point running median.^9^

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

The primary outcome was acute kidney injury (AKI) by the creatinine criteria of KDIGO:^10^
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
  fitted on the same patients.^11^
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
  transducer-offset artefacts after Li et al.^12^ were inserted into clean segments.
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
