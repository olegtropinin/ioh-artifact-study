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

Post hoc, the excess:
- was present at regularly cycled readings (12.2% of windows), which are probably automatic,
  as well as at irregular ones (17.0%);
- was larger with radial catheters (13.9% vs 1.8% at other times; 2,219 patients) than with
  pedal or femoral catheters, which an arm cuff cannot occlude (9.7% vs 3.4%; 58 patients;
  per-patient Mann–Whitney p < 0.001);
- was larger with right than with left radial catheters. In 60% of patients with a right and
  31% with a left radial catheter, at least 10% of arterial windows in the minute before cuff
  readings were artefact.

The 4.3% baseline 4–5 min before a reading is above the 1.8% seen at other times because it
includes the previous cuff cycle. The cuff arm is not recorded in VitalDB.

## Spurious and masked hypotension

At the per-minute median resolution (R3) with filter F1, 0.66% (95% CI 0.58–0.74) of recorded
minutes with MAP below 65 mmHg were spurious (Figure 3; Table S1). Spurious fractions were
higher:
- with one instantaneous value per minute (R2): 3.3% (3.0–3.6), which is 4–10 times the R3
  value for filters F0–F5;
- with the raw 2-s stream (R1): 2.0% (1.9–2.2).

Filters F3–F5 removed most spurious minutes at R1 and R3 (0.3–0.9%), but not at R2
(1.8–3.3%). The 7-point running median (F6) behaved differently from every other filter:
- it created spurious minutes: 7.5% at R3 and 9.9% at R2;
- it masked 20% (R3) to 24% (R2) of true hypotensive minutes.

**Binary exposure.** Against the reference at the same resolution, "≥ 10 min below 65 mmHg"
was classified with κ 0.95–0.99 by every filter except F6 at R2–R5 (Table S2). With F1 × R3, 38 of
3,249 patients (1.2%; 33 in the AKI set) changed exposure category, 32 of them upwards; 30 of the 38 had 5–10
reference minutes.

Resolution changed exposure prevalence more than any filter. In the reference series itself,
42.4% of patients were exposed at R3, 51.2% at R4 and 53.2% at R5.

The 7-point median applied to charted data erased most exposure: κ was 0.39 at R4 and 0.20
at R5.

## Which recorded low-pressure episodes are waveform-flagged

Of 106,725 recorded episodes of MAP below 65 mmHg in 3,123 patients:
- 8,471 (7.9%) were waveform-flagged;
- 3,909 (3.7%) were guard-dominated;
- 94,345 (88.4%) were physiological.

Flagged episodes accounted for 4.3% of hypotensive minutes. The proportion flagged depended
steeply on final duration and nadir (Table 2):
- 65–90% of episodes lasting ≤ 60 s with a nadir below 40 mmHg;
- 59–65% of episodes lasting ≤ 30 s with a nadir of 40–54 mmHg;
- ≤ 2.4% of episodes with a nadir of 55–64 mmHg;
- ≤ 2% of episodes lasting more than 1 min with a nadir ≥ 40 mmHg.

Final duration is not known while an episode unfolds. Post hoc, we therefore also looked at
episodes still below 65 mmHg after a given time, by the nadir so far (Table S3):

| Nadir so far | at 10 s | at 30 s | at 60 s | at 120 s |
|---|---|---|---|---|
| 20–39 mmHg | 79% flagged | 57% | 8% | 2% |
| below 20 mmHg | 75% | 59% | 44% | 29% |

A single rule, a fall of more than 20 mmHg from the preceding 30-s maximum, identified flagged
episodes in a validation half of patients with:
- sensitivity 0.89;
- specificity 0.92;
- positive predictive value 0.46.

This specificity came from trivial dips. Across all episodes with a nadir below 40 mmHg it was
0.07.

## Validation of the reference

**Cuff pressure.** The pre-specified check used a cuff MAP within 3 min of an episode. The cuff
MAP was ≥ 70 mmHg in:
- 84% (95% CI 83–85) of 4,506 flagged episodes;
- 46% (45–47) of 10,967 physiological episodes.

Restricting post hoc to deep episodes (nadir below 40 mmHg) and a cuff value within 60 s, the
cuff MAP was ≥ 70 mmHg in 81% (79–82) of 2,081 flagged episodes and 28% (24–32) of 443
physiological ones. Two consequences follow:
- about one flagged deep episode in five had a low cuff pressure nearby and may have been
  real;
- some deep episodes classed as physiological were probably artefact that the classifier
  missed.

**Pulse.** In non-pulsatile windows:
- the ECG rate was 40–150 min^−1^ in 97.8% of 153,662 windows;
- the plethysmographic pulse rate was in that range in 92.6%.

An ECG rate alone cannot exclude pulseless electrical activity. A plethysmographic pulse was
present in deep flagged and deep physiological episodes alike (98% and 97.5% of windows).

**Atrial fibrillation.** The non-pulsatile fraction was not higher in the 13 patients with
preoperative atrial fibrillation (0.17% vs 0.68%).

**Injection–recovery** (Table S8). Detected: flushes lasting ≥ 2 s or reaching 250 mmHg,
open-transducer levels up to 25 mmHg, and sampling. Rarely or never detected: short flushes of
200 mmHg or less, over-damping, partial occlusion (except severe), drift and ringing.

**Blinded AI rating** (secondary; Table S9). Agreement was 97.7% (κ 0.95; n = 131 after
excluding guard and "unsure").

## Association with acute kidney injury

**The reference association.** For ≥ 10 min below 65 mmHg the odds ratio for AKI was:
- crude: 1.65 (1.09–2.51);
- adjusted for age, eGFR, ASA and emergency: 1.46 (0.95–2.25);
- fully adjusted: 0.94 (0.60–1.48);
- fully adjusted without anaesthesia duration: 1.10 (0.70–1.71).

Because this exposure is cumulative, adjusting for duration removes part of its variance.

Other exposures were associated with AKI after full adjustment (Table S11):
- ≥ 10 min below 60 mmHg: 1.71 (1.04–2.79);
- area below 65 mmHg: 1.24 per 100 mmHg·min (1.07–1.45);
- time-weighted average below 65 mmHg: 1.27 per mmHg (1.00–1.60).

For ≥ 10 min below 55 mmHg the odds ratio was 1.95 (0.89–4.27), and per 10 min below 65 mmHg
it was 1.08 (0.99–1.17).

**Primary estimand.** With F1 × R3 the fully adjusted odds ratio was 0.90 (0.57–1.42). The ROR
was 0.96 (95% CI 0.86–1.06; permutation p = 0.42), and the pre-specified verdict was
equivalent.

The contrast rested on the 33 patients in the AKI set whose exposure category differed: 28
moved up and 5 moved down. None developed AKI, against 1.6 expected from the adjusted reference
model. The verdict depends on how many of the 28 upward-moved patients developed AKI (post hoc;
Table S7):

| AKI cases among the 28 | ROR (95% CI) | Verdict |
|---|---|---|
| 0 (observed) | 0.96 (0.86–1.07) | equivalent |
| 1 | 1.01 (0.90–1.14) | equivalent |
| 2 | 1.07 (0.90–1.27) | inconclusive |
| 3 | 1.13 (0.94–1.36) | inconclusive |

Under the reference model, two or more cases would have occurred with probability 0.36. The
equivalence verdict is therefore fragile.

In simulations from the adjusted reference model, the interval rule declared equivalence:
- in 82% of datasets without differential error;
- in 5% of datasets where differential error placed the median ROR at 1.24.

**Where the reference association was present** (post hoc). The pipeline and reference
estimates were close:

| Exposure | ROR (95% CI) |
|---|---|
| ≥ 10 min below 60 mmHg | 0.98 (0.85–1.15) |
| Area below 65 mmHg | 1.00 (0.97–1.03) |
| Time-weighted average below 65 mmHg | 1.01 (0.95–1.06) |

At 55 mmHg the binary ROR was imprecise: 1.28 (0.81–2.02) with F1 and 1.10 (0.84–1.45) with
F3. The pipeline odds ratio, 2.49 (1.22–5.08), crossed nominal significance where the
reference, 1.95 (0.89–4.27), did not.

Per 10 min below 65 mmHg the pipeline slope was 1.09 (1.00–1.18) against 1.08 (0.99–1.17) for
the reference. The difference in log-odds was 0.007 (−0.005 to 0.019).

**All 35 filter × resolution cells** (Table 3; Figure 4). No 95% interval or simultaneous band
excluded 1. Twenty-five cells were equivalent pointwise and 19 under simultaneous bands. The
ten inconclusive cells were:
- F0–F2 at R1;
- F2, F3, F4 and F6 at R2;
- F6 at R3–R5.

Four cells at R2 lay within 0.002 of the upper margin, two on each side. Excluding F6, the
point estimates ranged from 0.94 to 1.12. Coarser resolution of the reference itself did not
detectably change the odds ratio: relative to R3 it was 0.93–1.10, with intervals from 0.76
to 1.42.

**Exposure metric** (Figures S2–S4; Table S4). Across 420 specifications the median ROR was 0.99
(IQR 0.95–1.01). Minute-based exposures were insensitive to processing (RORs 0.92–1.02).
Area-based exposures below 55 mmHg were not:
- without a filter, 37% of the total area below 55 mmHg was artefact, half of it in 1% of
  patients;
- with F1 it was 13%, and with F3 none;
- the corresponding RORs were large but imprecise (post hoc; time-weighted average, F0:
  0.30, 0.06–1.53).

The interval for the odds ratio excluded 1 in 181 of 420 pipeline specifications and in 33 of
105 reference specifications. In 90 specifications, mostly area-based, the pipeline and the
reference differed in statistical significance.

**Sensitivity analyses** (Table S5). Of 16 sensitivity analyses with an interval, 14 were
equivalent (RORs 0.94–0.97, intervals within 0.83–1.10). These included the pre-specified S4
and S6, the exclusion of gynaecology and the disease-risk score.

Two were inconclusive:
- the waveform-mean reference (pre-specified), 0.74 (0.48–1.16). It changes calibration as
  well as cleaning, so it does not isolate artefact handling, and we cannot exclude a real
  difference;
- the numerics-defined monitoring period, 0.91 (0.75–1.11).

Adjustment for blood loss and for the number of creatinine measurements, and AKI stage ≥ 2,
gave point estimates of 0.95–0.97 without intervals. The creatinine count follows surgery and
is exploratory.

**Differential misclassification** (Table S6). Spurious hypotension on the raw stream was
unrelated to how often arterial blood was sampled (Spearman ρ 0.005, p = 0.81), and weakly,
inversely correlated with ASA class (ρ −0.06, p = 0.006).

Adjusted for reference exposure, the odds ratio for AKI was:
- 0.93 (0.74–1.16) per SD of spurious minutes;
- 0.59 (0.12–2.86) per unit of log(1 + minutes per hour).

The pre-specified negative control, fitted in the same model, gave 1.17 (0.96–1.43) per SD;
fitted separately it gave 1.16 (0.95–1.42). These estimates are imprecise. They show no
evidence of differential error but cannot exclude a modest amount.
