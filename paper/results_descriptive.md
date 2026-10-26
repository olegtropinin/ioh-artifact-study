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
at 25% of windows, against a baseline of 4.6% (Figure 5; 15,643 readings with a complete
−120 to +30 s window) — the time course of cuff
inflation on the cannulated arm.

## Spurious and masked hypotension

At the per-minute median resolution most commonly used in retrospective work (R3), 0.66%
(95% CI 0.58–0.74) of recorded minutes with MAP < 65 mmHg after the F1 filter were spurious
— the waveform-verified reference was ≥ 65 mmHg (Figure 2; Table S2). Spurious fractions were
higher with instantaneous sampling: 3.3% (3.0–3.6) with one value per minute (R2) and 2.0%
(1.9–2.2) with the raw 2-s stream (R1). The published filters F3–F5 removed most spurious
minutes at R1 and R3 (0.3–0.9%) but not at R2 (1.8–3.1%), where a single sampled value per
minute either catches an artefact or not. The 7-point running median (F6) behaved
differently from every other filter: it *created* spurious minutes (7.5% at R3, 9.9% at R2)
and masked 22% (R3) to 28% (R2) of true hypotensive minutes, because it delays and truncates
episodes.

**Binary exposure.** Against the reference at matched resolution, the binary exposure
"≥ 10 min with MAP < 65 mmHg" was classified with sensitivity ≥ 0.99, specificity
0.95–0.99 and κ 0.95–0.99 for every filter except F6 (Table S3). With F1 at R3, 38 of 3,249
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
artefact depended steeply on its depth and duration (Table 3; Figure 4):
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
