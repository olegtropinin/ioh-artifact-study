# Results

## Participants

Of 3,645 cases with an arterial waveform track, 3,434 had a retrievable waveform and 3,429 had
a monitoring period. The descriptive cohort comprised 3,249 patients. Together they had
11,466 h of monitoring, a median of 193 min per patient (IQR 134–272).

The AKI analysis set comprised 2,563 patients, of whom 91 (3.6%) developed AKI (Figure S1;
Table 1). Inclusion in the AKI set depended on postoperative creatinine testing. Of
non-transplant patients in the descriptive cohort, the AKI set included:
- 96% of thoracic patients;
- 97% of urology patients;
- 85% of general surgery patients;
- 28% of gynaecology patients.

## How much of the arterial record is artefact

Within the monitoring period, 96.3% of 2-s windows were valid. Artefact proper accounted for
2.3%:
- *high* 1.2%;
- *non-pulsatile* 0.7%;
- *noise* 0.2%;
- *zero* 0.07%.

Guard margins accounted for a further 1.4%. Inside the monitoring period the waveform was
never missing: the analogue channel records continuously, and the period is bounded by valid
data.

Artefact events were common:

| Artefact type | Patients with at least one event | Events per monitored hour |
|---|---|---|
| Flush | 98% | 2.6 |
| Noise | 97% | 2.7 |
| Non-pulsatile run | 90% | 2.0 |
| Zeroing | 33% | 0.2 |

In valid windows, monitor MAP and the waveform mean differed by more than 10 mmHg in a median
of 0.5% of windows per patient.

**Artefact around cuff measurements** (Figure 2). In 2,579 patients with both arterial and
cuff pressure, 14.0% of arterial windows in the 60 s before a new cuff value were labelled
artefact, against 1.8% at other times (19,560 readings). The excess peaked 22 s before the
value appeared, during the oscillometric cycle. At the peak 25.8% of windows were artefact,
against 4.3% 4–5 min earlier.

The peak was almost entirely *non-pulsatile* trace: 22.4% against 1.7% at baseline. Flush
labels barely rose (2.3% against 1.7%).

In post hoc analyses the excess was:
- **Present at regularly cycled readings**, which are probably automatic (12.2% of windows),
  as well as irregular ones (17.0%).
- **Larger with radial than with pedal or femoral catheters**, which an arm cuff cannot
  occlude: 13.9% against 1.8% at other times, compared with 9.7% against 3.4% (p < 0.001).
- **Larger with right than with left radial catheters.** Artefact preceded at least 10% of
  cuff readings in 60% of patients with right radial catheters and 31% of those with left.

The cuff arm is not recorded in VitalDB.

## Spurious and masked hypotension

At the per-minute median resolution (R3) with filter F1, 0.66% (95% CI 0.58–0.74) of recorded
minutes with MAP below 65 mmHg were spurious (Figure 3; Table S1). Spurious fractions were
higher:
- with one instantaneous value per minute (R2): 3.3% (3.0–3.6), which is 4–10 times the R3
  value depending on the filter;
- with the raw 2-s stream (R1): 2.0% (1.9–2.2).

Filters F3–F5 removed most spurious minutes at R1 and R3 (0.3–0.9%), but not at R2
(1.8–3.3%). The 7-point running median (F6) behaved differently from every other filter:
- it created spurious minutes: 7.5% at R3 and 9.9% at R2;
- it masked 20% (R3) to 24% (R2) of true hypotensive minutes.

**Binary exposure.** Against the reference at the same resolution, "≥ 10 min below 65 mmHg"
was classified with κ 0.95–0.99 by every filter except F6 (Table S2). With F1 × R3, 38 of
3,249 patients (1.2%) changed exposure category, 32 of them upwards; 30 of the 38 had 5–10
reference minutes.

Resolution changed exposure prevalence more than any filter. In the reference series itself,
42.4% of patients were exposed at R3, 51.2% at R4 and 53.2% at R5.

The 7-point median applied to charted data erased most exposure: κ was 0.39 at R4 and 0.20
at R5.

## Which recorded low-pressure episodes are artefact

Of 106,725 recorded episodes of MAP below 65 mmHg in 3,123 patients:
- 8,471 (7.9%) were waveform-flagged;
- 3,909 (3.7%) were guard-dominated;
- 94,345 (88.4%) were physiological.

Flagged episodes accounted for 4.3% of hypotensive minutes. The probability that an episode
was flagged depended steeply on its final duration and nadir (Table 2):
- episodes lasting ≤ 60 s with a nadir below 40 mmHg were flagged in 65–90%;
- brief episodes (≤ 30 s) with a nadir of 40–54 mmHg were flagged in 59–65%;
- episodes with a nadir of 55–64 mmHg were flagged in ≤ 2.4%;
- episodes lasting more than 1 min with a nadir ≥ 40 mmHg were flagged in ≤ 2%.

Final duration is unknown while an episode is unfolding. For episodes still below 65 mmHg after
a given time, the proportion flagged depended on the lowest pressure reached so far (post hoc,
Table S3):

| Nadir so far | 10 s | 30 s | 60 s | 120 s |
|---|---|---|---|---|
| 20–39 mmHg | 79% | 57% | 8% | 2% |
| Below 20 mmHg | 75% | 59% | 44% | 29% |

A simple rule, a fall of more than 20 mmHg from the preceding 30-s maximum, identified flagged
episodes with sensitivity 0.89 and specificity 0.92 in a validation half. Its specificity was
carried by trivial dips: among episodes with a nadir below 40 mmHg, specificity fell to 0.07.

## Validation of the reference

**Cuff MAP.** Among deep episodes (nadir below 40 mmHg), a cuff MAP within 60 s was ≥ 70 mmHg
in 81% (95% CI 79–82) of 2,081 flagged episodes, against 28% (24–32) of 443 physiological
ones.

**Pulse during flat or deep traces.** During flagged deep episodes the plethysmographic pulse
rate was in the physiological range in 98% of windows. During 153,662 non-pulsatile windows
the ECG heart rate was 40–150 min^−1^ in 97.8%. Circulation therefore continued while the
arterial trace was flat.

**Atrial fibrillation.** The non-pulsatile fraction was not higher in the 13 patients with
preoperative atrial fibrillation (0.17% against 0.68%).

**Injection–recovery** (Table S8). The classifier detected every injected flush lasting at
least 2 s or reaching 250 mmHg, every open-transducer level up to 25 mmHg, and every sampling
episode. It rarely or never detected:
- short flushes of 200 mmHg or less;
- over-damping;
- partial occlusion, except severe;
- slow drift;
- ringing.

**Blinded AI rating** (secondary; Table S9). Agreement with the classifier was 97.7%
(κ 0.95).

## Association with acute kidney injury

**The reference association.** For ≥ 10 min below 65 mmHg the odds ratio for AKI was:
- crude: 1.65 (1.09–2.51);
- age, eGFR, ASA and emergency adjusted: 1.46 (0.95–2.25);
- fully adjusted: 0.94 (0.60–1.48).

Removing anaesthesia duration from the adjustment set did not change the fully adjusted
estimate. For 55 mmHg the fully adjusted odds ratio was 1.95 (0.89–4.27), and per 10 min
below 65 mmHg it was 1.08 (0.99–1.17) (Table S11).

**Primary estimand.** With F1 × R3 the fully adjusted odds ratio was 0.90 (0.57–1.42). The ROR
was 0.96 (95% CI 0.86–1.06; permutation p = 0.42): equivalent.

The contrast rested on the 33 patients whose exposure category differed: 28 moved up and 5
moved down. None of them developed AKI, against 1.6 expected from the adjusted reference model
(probability of none 0.19).

Had AKI occurred in k of the 28 upward-moved patients, the ROR would have been:

| k | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| ROR | 0.96 | 1.01 | 1.07 | 1.13 | 1.20 | 1.27 |

Equivalence would have been lost only from about five cases onwards (Table S7).

In simulations from the adjusted reference model, the interval rule declared equivalence:
- in 82% of datasets without differential error;
- in 5% of datasets with differential error that placed the median ROR at 1.24.

The interval covered 1 in 97–100% of independent outcome permutations.

**All 35 filter × resolution cells** (Table 3; Figure 4). No 95% interval or simultaneous band
excluded 1. Twenty-five cells were equivalent pointwise and 19 under simultaneous bands.

Four cells at R2 sat within 0.002 of the upper margin, two on each side of it. The inconclusive
cells were:
- the raw 2-s stream (R1);
- instantaneous per-minute sampling (R2);
- the 7-point median.

With any filter other than F6, the point estimates ranged from 0.94 to 1.12. Coarser
resolution of the reference itself did not detectably change the odds ratio: relative to R3,
the ratios were 0.93–1.10, with intervals between 0.76 and 1.42.

**Where the reference association was stronger** (post hoc). At 55 mmHg the binary ROR was
imprecise:
- F1: 1.28 (0.81–2.02);
- F3: 1.10 (0.84–1.45).

At 60 mmHg it was 0.95–0.98, with intervals of 0.79–1.15. The slope per 10 min below 65 mmHg
was 1.09 with F1 × R3 against 1.08 with the reference. The difference in log-odds was 0.007
(−0.005 to 0.019).

**Exposure metric** (Figures S2–S4; Table S4). Across all 420 specifications the median
ROR was 0.99 (IQR 0.95–1.01).
- Minute-based exposures were insensitive to processing (RORs 0.92–1.02).
- Area-based exposures below 55 mmHg were not. Without a filter, 37% of the total area below
  55 mmHg was artefact, half of it in 1% of patients. With F1 the share was 13%, and with F3
  it was none. The corresponding RORs were large but imprecise (post hoc; time-weighted
  average, F0: 0.30, 0.06–1.53).
- For 90 specifications, mostly area-based, the pipeline and the reference differed in
  whether their odds ratio was statistically significant.

**Sensitivity analyses** (Table S5). The primary ROR ranged from 0.94 to 0.97 across the
reference variants, adjustment variants, S4, S6, the exclusion of gynaecology and the
disease-risk score. All intervals lay within 0.83–1.10. The adjustments for blood loss and
for creatinine count, and AKI stage ≥ 2, have point estimates only. The exceptions were the
waveform-mean reference, 0.74 (0.48–1.16), whose monitor–waveform calibration differences the
primary design deliberately avoided, and the numerics-defined period, 0.91 (0.75–1.11).

**Differential misclassification** (Table S6). Spurious hypotension was unrelated to how often
arterial blood was sampled (Spearman ρ 0.005, p = 0.81). Adjusted for reference exposure, the
odds ratio for AKI per SD of spurious minutes on the raw stream was 0.93 (0.74–1.16); per unit
of log(1 + minutes per hour) it was 0.59 (0.12–2.86). The negative control, fitted separately,
gave 1.16 (0.95–1.42) per SD. These estimates are imprecise and cannot exclude modest
differential error, but they gave no sign of it.
