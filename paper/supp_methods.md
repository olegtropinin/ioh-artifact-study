# Supplementary Methods

## S1. Waveform features and classifier

**Features.** For every 2-s window of the 500 Hz waveform we computed:
- the fraction of finite samples;
- the mean, minimum, maximum, 2nd, 10th, 90th and 98th centiles;
- the median absolute second difference;
- the number of systolic upstrokes in the window and in the centred 6-s window.

An upstroke is a rise of more than 8 mmHg within 100 ms after 20-ms smoothing; successive
upstrokes are at least 250 ms apart.

**Labels.** The labels, thresholds and guard margins are given in the Methods.

**Cases without a waveform.** Of 3,645 cases with a listed waveform track, 211 returned no
waveform through the VitalDB API on 26 October 2026. Their case identifiers are released with
the code.

**Threshold tuning.** The noise threshold, the upstroke rule and the guard length were set by
inspecting outcome-free descriptive data from fewer than 600 cases during development. The
rule discarded before the freeze (beat-lag autocorrelation) labelled 12% of windows as
non-pulsatile in patients with atrial fibrillation against 1% in sinus rhythm, at pulse
pressures of 56–83 mmHg.

## S2. Interval for the ratio of odds ratios (amendment A15)

**Why the bootstrap failed.** Exposure categories under F1 × R3 and the reference differed in
33 of 2,563 patients. Bootstrap resamples change few of these patients, so the bootstrap
distribution of log ROR is spiky and its central 95% is narrow. In 100 permutations of the
outcome, under which the true ROR is exactly 1, the percentile interval covered 1 in 51% of
datasets for F1 × R3, 79% for F0 × R1, 89% for F3 × R2 and 91% for F6 × R3.

**The rule.** Before the real outcome was examined, a written rule set every ROR-type interval
to log ROR ± z × max(bootstrap SE, permutation-null SD). The permutation-null SD came from
200 permutations of the analysed outcome. The same SE was used for the simultaneous bands,
whose critical value is the bootstrap max-|z| over the 35 cells (3.22).

**Coverage check.** The SD was estimated from 200 permutations in the dry run, independent of
the 100 calibration datasets. With that SD, the interval covered 1 in 100%, 99%, 100% and 97%
of calibration datasets for the four pairs.

**Operating characteristics at the margin.** Outcomes were simulated from the fully adjusted
reference model, adding a log-odds shift γ in the patients moved upwards by the pipeline. We
chose γ = 1.91 so that the median simulated ROR was 1.24. In 200 datasets, each analysed with
the full rule (200 bootstrap resamples and 200 permutations), equivalence was declared in 5%.
Without differential error (γ = 0) it was declared in 82%, and the interval covered 1 in 97%.

Reaching the lower margin requires almost all five downward-moved patients to develop AKI. The
SD of log ROR under the simulated alternative (0.098) exceeded that under the null (0.062).
The bootstrap SE, which grows with the number of cases among the discordant patients, then
dominates the rule.

## S3. Blinded AI rating

The 400-snippet adjudication set has five strata:
- 100 low-MAP windows flagged as artefact;
- 50 low-MAP windows labelled guard only;
- 100 low-MAP windows labelled valid;
- 100 random valid windows;
- 50 flagged windows with MAP ≥ 65 mmHg.

There are at most two snippets per patient. A subset of 152 snippets was shown, as 26 grids of
six 40-s waveform panels, to two independent instances of an AI model (Claude, Anthropic). The
grids were in a folder that contained no key, code or labels. The raters could read files,
were instructed to open only the listed images, and saw only the waveform.

The prompt is released with the code. The subset is enriched for artefact (43% against 3.7%
in the data), which inflates κ.

## S4. Injection–recovery

The implementation check used 296 clean 2-min segments from 100 cases. Synthetic flush,
zeroing, sampling, damping, noise and offset artefacts, after Li et al., were injected in the
middle 20 s.

The post hoc sweep used 119 segments from 60 cases. It varied:
- flush amplitude (120–300 mmHg) and duration (0.5–4 s);
- open-transducer level (0–25 mmHg);
- damping cut-off (1.5–10 Hz);
- partial occlusion (pulse pressure scaled to 0.5–0.15);
- linear drift (10–40 mmHg over 20 s);
- 18-Hz ringing (5–20 mmHg);
- sampling without a terminal flush.

Detection counted only artefact labels, not guard. Clean segments were selected as valid by
the classifier, so the absence of false labels in uninjected segments holds by construction.

## S5. Real-time episode table

For each episode and each elapsed time t (10, 30, 60 and 120 s), the nadir so far was the
lowest monitor MAP in the first t seconds. Episodes shorter than t were not counted at t. The
table therefore gives the probability that an episode is flagged, given that it has lasted at
least t seconds and reached a given nadir.

## S6. Pipeline filters and sensitivity analyses

Filters were applied to the 2-s monitor numerics (F5 and F6 after sampling, on the pipeline's
own grid):
- F0: none;
- F1: MAP below 20 or above 250 mmHg removed;[@leesb]
- F2: MAP below 30 or above 200 mmHg removed;[@khan]
- F3: systolic above 250, diastolic below 15, MAP below 35 or above 150, or pulse pressure
  below 15 mmHg removed;[@jacobsson]
- F4: physiological consistency (MAP below 20 or above 200; systolic below 20 or above 300;
  systolic ≤ diastolic; pulse pressure below 5; diastolic below 5);
- F5: F4, then removal of values that differ from both neighbours by more than 30 mmHg;[@du]
- F6: F4, then a 7-point running median.[@pasma2020]

The *noise* label also requires a median absolute second difference of the waveform of at
least 4 mmHg; the *zero* range is the 2nd–98th centile range; an upstroke is a rise of more
than 8 mmHg within 100 ms.

Pre-specified sensitivity analyses varied the reference (guard length 0 s and 6/30 s,
pulse-pressure threshold 5 and 12 mmHg, minute validity 25% and 75%, no bridging, and the
waveform mean in place of the monitor value), the monitoring period (defined from the numerics),
the adjustment set (blood loss; number of postoperative creatinine measurements) and the
outcome (AKI stage ≥ 2; missing postoperative creatinine counted as no AKI, S4;
transplantation included, S6).

## S7. Further results

**Inclusion in the AKI set by department** (non-transplant patients of the descriptive cohort):
thoracic 96%, urology 97%, general surgery 85%, gynaecology 28%.

**Artefact events.** Guard margins were 1.4% of windows. Inside the monitoring period the
waveform was never missing: the analogue channel records continuously, and the period is
bounded by valid data. In valid windows, monitor MAP and the waveform mean differed by more
than 10 mmHg in a median of 0.5% of windows per patient.

| Artefact type | Patients with at least one event | Events per monitored hour |
|---|---|---|
| Flush | 98% | 2.6 |
| Noise | 97% | 2.7 |
| Non-pulsatile run | 90% | 2.0 |
| Zeroing | 33% | 0.2 |

**Cuff cycle.** At the peak, 22 s before a new cuff value, 25.8% of arterial windows were
artefact, against 4.3% 4–5 min earlier; flush labels barely rose (2.3% against 1.7%). The 4.3%
baseline is above the 1.8% seen at other times because it includes the previous cuff cycle.
Post hoc, the excess was present at regularly cycled readings (12.2% of windows), which are
probably automatic, as well as at irregular ones (17.0%). In 60% of patients with a right and
31% with a left radial catheter, at least 10% of arterial windows in the minute before cuff
readings were artefact.

**Episodes.** Of 106,725 recorded episodes, 3,909 (3.7%) were guard-dominated and 94,345
(88.4%) physiological. Flagged proportions were 59–65% for episodes lasting ≤ 30 s with a nadir
of 40–54 mmHg.

**Pulse.** An ECG rate alone cannot exclude pulseless electrical activity. A plethysmographic
pulse was present in deep flagged and deep physiological episodes alike (98% and 97.5% of
windows). The non-pulsatile fraction was 0.17% in the 13 patients with preoperative atrial
fibrillation and 0.68% in the others.

**Injection–recovery.** Short flushes of 200 mmHg or less were rarely detected; partial
occlusion was detected only when severe (Table S8).

**Association with AKI.** For ≥ 10 min below 55 mmHg the reference odds ratio was 1.95
(0.89–4.27), and per 10 min below 65 mmHg 1.08 (0.99–1.17); the pipeline slope was 1.09
(1.00–1.18), a difference in log-odds of 0.007 (−0.005 to 0.019). Four of the 35 filter ×
resolution cells at R2 lay within 0.002 of the upper margin, two on each side; excluding F6,
point estimates ranged from 0.94 to 1.12, and the resolution effect on the reference had
intervals from 0.76 to 1.42. The interval for the odds ratio excluded 1 in 181 of 420 pipeline
specifications and in 33 of 105 reference specifications.

**Sensitivity analyses.** The 14 equivalent analyses had intervals within 0.83–1.10 and
included the exclusion of gynaecology and adjustment for a disease-risk score. Adjustment for
blood loss and for the number of creatinine measurements, and AKI stage ≥ 2, gave point
estimates of 0.95–0.97 without intervals; the creatinine count follows surgery and is
exploratory. The waveform-mean reference changes calibration as well as cleaning, so it does
not isolate artefact handling, and a real difference cannot be excluded.

**Differential misclassification.** Spurious hypotension was weakly and inversely correlated
with ASA class (ρ −0.06, p = 0.006). The odds ratio per unit of log(1 + minutes per hour) was
0.59 (0.12–2.86). The negative control fitted separately gave 1.16 (0.95–1.42) per SD.
