# Results

## Participants

Of 3,645 cases with an arterial waveform track, 3,429 had a retrievable waveform and a
monitoring period. The descriptive cohort comprised 3,249 patients with a median of 193 min of
monitoring (IQR 134–272). The AKI analysis set comprised
2,563 patients, of whom 91 (3.6%) developed AKI (Table 1; Fig. S1 in Online Resource 1). Inclusion in the AKI set
depended on postoperative creatinine testing: it included 85–97% of non-transplant patients in
general, thoracic and urological surgery but 28% in gynaecology.

## How much of the arterial record is artefact

Within the monitoring period, 96.3% of 2-s windows were valid. Artefact proper accounted for
2.3% (*high* 1.2%, *non-pulsatile* 0.7%, *noise* 0.2%, *zero* 0.07%) and guard margins for a
further 1.4%. Artefact events were nonetheless common: 98% of patients had at least one flush
and 90% a non-pulsatile run (Online Resource 1).

**Artefact around cuff measurements** (Fig. 2). In 2,579 patients with both arterial and
cuff pressure, 14.0% of arterial windows in the 60 s before a new cuff value were labelled
artefact, against 1.8% at other times (19,560 readings). The excess peaked 22 s before the
value appeared, during the oscillometric cycle, at 25.8% of windows, and was almost entirely
*non-pulsatile* trace (22.4% against 1.7% at baseline). Post hoc, it was larger with radial catheters
(13.9% vs 1.8%; 2,219 patients) than with pedal or femoral catheters, which an arm cuff cannot
occlude (9.7% vs 3.4%; 58 patients; p < 0.001), and with right than left radial catheters
(Online Resource 1). The cuff arm is not recorded in VitalDB.

## Spurious and masked hypotension

At the per-minute median resolution (R3) with filter F1, 0.66% (95% CI 0.58–0.74) of recorded
minutes with MAP below 65 mmHg were spurious (Fig. 3; Table S1). With one instantaneous value
per minute (R2) the fraction was 3.3% (3.0–3.6), 4–10 times the R3 value for filters F0–F5,
and with the raw 2-s stream (R1) 2.0% (1.9–2.2). Filters F3–F5 removed most spurious minutes at
R1 and R3 (0.3–0.9%), but not at R2 (1.8–3.3%). The 7-point running median (F6) behaved
differently from every other filter: it created spurious minutes (7.5% at R3, 9.9% at R2) and
masked 20% (R3) to 24% (R2) of true hypotensive minutes.

**Binary exposure.** Against the reference at the same resolution, "≥ 10 min below 65 mmHg"
was classified with κ 0.95–0.99 by every filter except F6 at R2–R5 (Table S2). With F1 × R3, 38
of 3,249 patients (1.2%; 33 in the AKI set) changed exposure category, 32 of them upwards; 30
of the 38 had 5–10 reference minutes. Resolution changed exposure prevalence more than any
filter: in the reference itself, 42.4% of patients were exposed at R3, 51.2% at R4 and 53.2% at
R5. The 7-point median applied to charted data erased most exposure (κ 0.39 at R4, 0.20 at R5).

## Which recorded low-pressure episodes are waveform-flagged

Of 106,725 recorded episodes of MAP below 65 mmHg in 3,123 patients, 8,471 (7.9%) were
waveform-flagged; they accounted for 4.3% of hypotensive minutes. The proportion flagged depended steeply on
final duration and nadir (Table 2): 65–90% of episodes lasting ≤ 60 s with a nadir below
40 mmHg, but ≤ 2.4% of episodes with a nadir of 55–64 mmHg and ≤ 2% of episodes lasting more
than 1 min with a nadir ≥ 40 mmHg.

Because final duration is not known while an episode unfolds, we also looked post hoc at
episodes still below 65 mmHg after a given time (Table S3). Of falls to 20–39 mmHg, 79% were
flagged at 10 s, 57% at 30 s and 8% at 60 s; falls below 20 mmHg were still flagged in 29% at
2 min.

A single rule, a fall of more than 20 mmHg from the preceding 30-s maximum, identified flagged
episodes in a validation half of patients with sensitivity 0.89, specificity 0.92 and positive
predictive value 0.46. This specificity came from trivial dips: across episodes with a nadir
below 40 mmHg it was 0.07.

## Validation of the reference

**Cuff pressure.** A cuff MAP within 3 min of an episode was ≥ 70 mmHg in 84% (95% CI 83–85) of
4,506 flagged episodes and 46% (45–47) of 10,967 physiological episodes. Restricting post hoc to
deep episodes (nadir below 40 mmHg) and a cuff value within 60 s, the proportions were 81%
(79–82) of 2,081 flagged and 28% (24–32) of 443 physiological episodes. About one flagged deep
episode in five may therefore have been real, and some "physiological" deep episodes were
probably missed artefact.

**Other checks** (Online Resource 1). In non-pulsatile windows the ECG rate was 40–150 min^−1^
in 97.8% and the plethysmographic pulse rate in 92.6% of 153,662 windows, and the non-pulsatile
fraction was not higher in atrial fibrillation. Injection–recovery detected flushes lasting
≥ 2 s or reaching 250 mmHg, open-transducer levels up to 25 mmHg and sampling, but rarely
over-damping, partial occlusion, drift or ringing (Table S8). The blinded AI rater agreed with
the classifier in 97.7% of snippets (κ 0.95; n = 131; Table S9).

## Association with acute kidney injury

**The reference association.** For ≥ 10 min below 65 mmHg the odds ratio for AKI was 1.65
(1.09–2.51) crude, 1.46 (0.95–2.25) adjusted for age, eGFR, ASA and emergency, 0.94 (0.60–1.48)
fully adjusted and 1.10 (0.70–1.71) fully adjusted without anaesthesia duration; because this
exposure is cumulative, adjusting for duration removes part of its variance. Other exposures
were associated with AKI after full adjustment (Table S11): ≥ 10 min below 60 mmHg, 1.71
(1.04–2.79); area below 65 mmHg, 1.24 per 100 mmHg·min (1.07–1.45); and time-weighted average
below 65 mmHg, 1.27 per mmHg (1.00–1.60).

**Primary estimand.** With F1 × R3 the fully adjusted odds ratio was 0.90 (0.57–1.42). The ROR
was 0.96 (95% CI 0.86–1.06; permutation p = 0.42), and the pre-specified verdict was
equivalent.

The contrast rested on the 33 patients in the AKI set whose exposure category differed: 28
moved up and 5 moved down. None developed AKI, against 1.6 expected from the adjusted reference
model. Post hoc, with one AKI case among the 28 upward-moved patients the
ROR would have been 1.01 (0.90–1.14), still equivalent, and with two 1.07 (0.90–1.27),
inconclusive (Table S7). Two or more cases had probability 0.36 under the reference model, so
the equivalence verdict is fragile. In simulations from the adjusted reference model, the interval
rule declared equivalence in 82% of datasets without differential error and in 5% of datasets
where differential error placed the median ROR at 1.24.

**Where the reference association was present** (post hoc), pipeline and reference estimates
were close: ROR 0.98 (0.85–1.15) for ≥ 10 min below 60 mmHg, 1.00 (0.97–1.03) for area below
65 mmHg and 1.01 (0.95–1.06) for time-weighted average below 65 mmHg. At 55 mmHg the binary ROR
was imprecise: 1.28 (0.81–2.02) with F1 and 1.10 (0.84–1.45) with F3; the pipeline odds ratio,
2.49 (1.22–5.08), crossed nominal significance where the reference, 1.95 (0.89–4.27), did not.

**All 35 filter × resolution cells** (Table 3; Fig. 4). No 95% interval or simultaneous band
excluded 1. Twenty-five cells were equivalent pointwise and 19 under simultaneous bands; the ten
inconclusive cells were F0–F2 at R1, F2–F4 and F6 at R2, and F6 at R3–R5. Coarser resolution of the
reference itself did not detectably change the odds ratio (0.93–1.10 relative to R3).

**Exposure metric** (Figs. S2–S4; Table S4). Across 420 specifications the median ROR was 0.99
(IQR 0.95–1.01), and minute-based exposures were insensitive to processing (0.92–1.02).
Area-based exposures below 55 mmHg were not: without a filter, 37% of the total area below
55 mmHg was artefact, half of it in 1% of patients (13% with F1, none with F3), and the
corresponding RORs were large but imprecise (post hoc). In 90 of 420 specifications, mostly
area-based, pipeline and reference differed in statistical significance.

**Sensitivity analyses** (Table S5). Of 16 sensitivity analyses with an interval, 14 were
equivalent (RORs 0.94–0.97), including the pre-specified S4 and S6. The two inconclusive ones were
the waveform-mean reference (0.74, 0.48–1.16), which also changes calibration, and the
numerics-defined monitoring period (0.91, 0.75–1.11).

**Differential misclassification** (Table S6). Spurious hypotension on the raw stream was
unrelated to how often arterial blood was sampled (Spearman ρ 0.005, p = 0.81). Adjusted for
reference exposure, the odds ratio for AKI was 0.93 (0.74–1.16) per SD of spurious minutes; the
negative control gave 1.17 (0.96–1.43). These estimates show no evidence of differential error
but cannot exclude a modest amount.
