---
title: "How much recorded intraoperative hypotension is arterial-line artefact, and does it bias the association with acute kidney injury? A waveform-referenced cohort study"
---

**Running title:** Arterial-line artefact and intraoperative hypotension

**Author:** Oleg Tropynin

**Affiliation:** Independent researcher, Karaganda, Kazakhstan

**Correspondence:** Oleg Tropynin, tropininoleg@gmail.com

**Keywords:** intraoperative hypotension; arterial pressure monitoring; artefact; acute
kidney injury; measurement error; non-invasive blood pressure; VitalDB

# Key points

- In 3,249 patients with continuous arterial monitoring, 2.3% of monitored time was artefact
  (3.7% including the margins around artefact). With per-minute medians and a range filter,
  0.7% of recorded minutes with mean arterial pressure (MAP) below 65 mmHg were spurious.
- In this cohort, ≥ 10 min of MAP below 65 mmHg was not independently associated with acute
  kidney injury (AKI). Artefact handling neither created nor removed an association, and
  artefact was not recorded preferentially in patients who developed AKI.
- Running-median smoothing and unfiltered area-under-threshold exposures distorted the
  measured hypotension. Over a third of the unfiltered area below 55 mmHg was artefact, half
  of it in 1% of patients.
- A recorded fall to 20–39 mmHg turned out to be artefact in 79% of cases when it had lasted
  10 s, 57% at 30 s and 8% at 60 s. A sudden fall should prompt a look at the waveform, not
  a delay in treatment.
- Arterial artefact rose sixfold during the non-invasive cuff cycle, mostly as a
  non-pulsatile trace. This is consistent with occlusion of the cannulated arm.

# Abstract

**Background.** Studies linking intraoperative hypotension to acute kidney injury (AKI) use
monitor numbers that include arterial-line artefacts. It is unknown how much recorded
hypotension is artefact, and whether artefact handling biases the association.

**Methods.** We analysed 3,249 adults in the open VitalDB dataset who had a 500 Hz arterial
waveform. Each 2-s monitor value was labelled from the waveform, giving a waveform-referenced
series. We compared this series with 420 retrospective processing pipelines (7 filters × 5
resolutions × 4 metrics × 3 thresholds). The primary estimand was the ratio of adjusted odds
ratios (ROR) for KDIGO AKI with ≥ 10 min of mean arterial pressure (MAP) < 65 mmHg. It
compared per-minute medians with a range filter against the reference, with an equivalence
margin of 0.80–1.25.

**Results.** Of monitored time, 96.3% was artefact-free. With per-minute medians, 0.7% of
recorded hypotensive minutes were spurious, against 3.3% with one instantaneous value per
minute. Of 2,563 patients in the AKI analysis, 91 (3.6%) developed AKI. The adjusted odds
ratio was 0.94 (95% CI 0.60–1.48) with the reference and 0.90 (0.57–1.42) with the
pipeline. The ROR was 0.96 (0.86–1.06), which was equivalent. Exposure differed in 33
patients, none of whom developed AKI. Spurious hypotension was not associated with AKI.
Arterial artefact rose from 4% to 26% during cuff measurement.

**Conclusions.** With per-minute medians and a range filter, artefact did not bias the
association between hypotension and AKI in this cohort, in which the association was null.
Running-median smoothing and unfiltered area-based exposures should be avoided.
