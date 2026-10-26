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
