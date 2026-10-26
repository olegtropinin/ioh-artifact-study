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
