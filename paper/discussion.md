# Discussion

## Principal findings

In 3,249 patients with a high-resolution arterial waveform, artefacts were frequent events but
a small part of recorded hypotension. With a per-minute median and a range filter, fewer than
1% of hypotensive minutes were spurious, and the exposure category changed in 1.2% of
patients.

For the pre-specified exposure, ≥ 10 min below 65 mmHg, the adjusted association with AKI was
null (odds ratio 0.94), so non-differential error had little to act on. The equivalence of
pipeline and reference (ROR 0.96) therefore mainly tests *differential* error. That is the
scenario in which artefact recorded preferentially in patients destined for AKI would
manufacture an association.

We found no evidence of it:
- none of the 33 patients whose category changed developed AKI;
- spurious hypotension was unrelated to blood sampling and showed no detectable association
  with AKI.

The verdict is fragile, however. Two AKI cases among the 28 patients moved upwards would have
made it inconclusive, and under the reference model such an outcome had a probability of about
one in three.

Two further observations support the robustness of duration-based exposures:
- *Where the reference showed an association* (≥ 10 min below 60 mmHg; area and time-weighted
  average below 65 mmHg), the pipeline estimates were within a few per cent of the reference
  (post hoc).
- *At 55 mmHg* the pipeline estimate was higher than the reference, but imprecise.

Three processing choices mattered more than the filter:
- **The 7-point running median.** It created spurious hypotension and masked a fifth of true
  hypotension.
- **Unfiltered area-based exposures below 55 mmHg.** Zero and flush values in a few patients
  inflated them: over a third of the area was artefact.
- **Resolution.** It changed the share of exposed patients by a fifth, without a detectable
  change in the odds ratio.

## Comparison with previous work

Pasma et al. found that the choice among eight filters changed the incidence of hypotension
up to twofold, but changed the association with myocardial injury little.[@pasma2020]
Jacobsson et al. showed against a waveform reference that coarse sampling inflates measured
hypotension.[@jacobsson] Both comparisons were between pipelines, or extrapolated to outcomes.

Our study adds:
- an external, waveform-referenced comparator at every resolution;
- a direct, pre-specified estimate of the outcome effect;
- a test for differential error.

We agree with both on duration-based exposures. Unlike Pasma et al., we found that the
7-point median distorts exposure substantially, even when the ratio of odds ratios stays near
1. The AWAKE trial showed that the monitoring method changes measured and treated hypotension
at induction.[@kouz] Our resolution results are the retrospective counterpart.

Wax et al.[@wax] and a recent preprint from the MOVER cohort[@liu] treated disagreement between
cuff and arterial pressure as clinical information. Arterial artefact rose sixfold during the
cuff cycle, mostly as a non-pulsatile trace. This is a measurement mechanism that generates
such disagreement. The pattern fits occlusion of the cannulated arm in part, because the
excess was:
- larger with radial than with lower-limb catheters;
- larger on the right than on the left;
- present at regularly cycled readings;
- mostly not flush.

A smaller excess with pedal and femoral catheters shows that this is not the whole
explanation. Studies of discordance should exclude arterial values from the cuff cycle, or
show that their results survive the exclusion.

Earlier work compared artefact detection algorithms with human annotation of stored
values,[@maleczek; @pasma2021] and a scoping review found no agreed reference standard for
arterial artefact.[@bergmann] Our approach uses the waveform only to decide whether a monitor
value can be trusted. It can be reproduced on any dataset that stores both.

## Implications

**For investigators:**
- Use a per-minute median with a range filter, or a rule such as F3, and report resolution as
  carefully as threshold.
- Do not use running-median smoothing to estimate exposure.
- Do not compute area- or time-weighted exposures below 55 mmHg from unfiltered data.
- In paired multiverse comparisons, check the operating characteristics of intervals before
  unblinding, at the null and at the decision margins. Permutation alone checks only the
  null. In our data, percentile intervals covered the truth in half of null datasets.

**For alarm design and retrospective cleaning:**
- These probabilities are retrospective and describe a population. They must not be used to
  delay treatment, and a sudden fall should be treated as real until the waveform shows
  otherwise.
- At 10 s, one in five falls to 20–39 mmHg was not flagged. One in five flagged deep episodes
  had a low cuff pressure within a minute.
- Many very brief, very deep recorded falls were waveform-flagged in retrospect (post hoc).
  A fall below 20 mmHg was still flagged in more than a quarter of cases at 2 min.
- An automated system could use such probabilities to *annotate* a probable artefact, never to
  *suppress* an alarm. A simple drop rule does not separate deep artefacts from deep real
  events: below 40 mmHg its specificity was 0.07.
- Where possible, the cuff should be placed on the limb opposite an arterial line.[@saugel]
  The cuff remains an essential cross-check of the arterial line.

## Strengths and limitations

The reference comes from the waveform recorded alongside the numbers and never replaces
monitor values. The protocol was frozen after a permuted dry run, and every later change is
documented. The reference was checked against independent signals, and all data and code are
public.

Limitations:
- **The equivalence verdict rests on few patients.** It rests on 33 discordant patients and
  would not have survived two AKI cases among them. It may not transfer to cohorts with more
  artefact or a stronger association.
- **No human rater adjudicated the reference.** The AI rater shares its model family with the
  classifier's designer and sees only the waveform. A 400-snippet set with a hidden key is
  released for human adjudication; it should show the monitor value as well.
- **The reference is *waveform-screened*, not error-free.** The classifier cannot see:
  - levelling errors and zero drift, about 7 mmHg per 10 cm, which matter in lateral and
    tilted positions;
  - most over-damping;
  - partial occlusion;
  - very short flushes.

  It also misses some artefact: 28% of deep "physiological" episodes had a cuff MAP ≥ 70 mmHg
  nearby.
- **No end-tidal carbon dioxide or vasopressor data.** We did not examine these around deep
  episodes.
- **Much post-induction hypotension was missed.** Monitoring started a median of 10 min after
  the start of anaesthesia.[@sudfeld]
- **One centre, few events.** The data come from a single centre in 2016–2017, mainly general
  and thoracic surgery, with 3.6% AKI by creatinine alone. Postoperative creatinine testing
  varied by department.
- **Adjustment.** The adjusted odds ratios depend on adjustment for anaesthesia duration,
  which partly removes cumulative exposure.
- **Simulated charting.** Charted resolutions were simulated, not taken from real
  records.[@kool]
- **Practice-dependent frequencies.** Artefact frequencies depend on local practice. The
  mechanisms, and the direction of the resolution and smoothing effects, should transfer.
