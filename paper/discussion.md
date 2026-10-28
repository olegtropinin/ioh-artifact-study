# Discussion

## Principal findings

Artefacts were frequent events but a small part of recorded hypotension: with a per-minute
median and a range filter, fewer than 1% of hypotensive minutes were spurious, and the exposure
category changed in 1.2% of patients.

For the pre-specified exposure, ≥ 10 min below 65 mmHg, the adjusted association with AKI was
null (odds ratio 0.94), so non-differential error had little to act on. The equivalence of
pipeline and reference (ROR 0.96) therefore mainly tests *differential* error: artefact
recorded preferentially in patients destined for AKI, which would manufacture an association.
We found no evidence of it. None of the 33 patients whose category changed developed AKI, and
spurious hypotension was unrelated to blood sampling and to AKI. The verdict is fragile,
however: two AKI cases among the 28 patients moved upwards would have made it inconclusive,
an outcome with a probability of about one in three under the reference model. Where the
reference did show an association (≥ 10 min below 60 mmHg; area and time-weighted average below
65 mmHg), the pipeline estimates were within a few per cent of the reference (post hoc).

Three processing choices mattered more than the filter. The 7-point running median created
spurious hypotension and masked a fifth of true hypotension. Unfiltered area-based exposures
below 55 mmHg were inflated by zero and flush values in a few patients: over a third of the
area was artefact. Resolution changed the share of exposed patients by a fifth, without a
detectable change in the odds ratio.

## Comparison with previous work

Pasma et al. found that the choice among eight filters changed the incidence of hypotension up
to twofold but the association with myocardial injury little;[@pasma2020] Jacobsson et al.
showed against a waveform reference that coarse sampling inflates measured
hypotension.[@jacobsson] We add a waveform-referenced comparator at every resolution, a
pre-specified estimate of the outcome effect and a test for differential error. We agree with
both on duration-based exposures; unlike Pasma et al., we found that the 7-point median
distorts exposure substantially even when the ratio of odds ratios stays near 1. The AWAKE
trial showed that the monitoring method changes measured and treated hypotension at
induction;[@kouz] our resolution results are the retrospective counterpart.

Wax et al.[@wax] and a recent preprint from the MOVER cohort[@liu] treated disagreement between
cuff and arterial pressure as clinical information. Arterial artefact rose sixfold during the
cuff cycle, mostly as a non-pulsatile trace, which is a measurement mechanism that generates
such disagreement. The pattern by catheter site fits occlusion of the
cannulated arm in part, but a smaller excess with pedal and femoral catheters shows that this
is not the whole explanation, and because VitalDB does not record the cuff arm, occlusion
remains a hypothesis. Studies of discordance should check whether their results
survive excluding arterial values from the cuff cycle.

Earlier work compared artefact algorithms with human annotation of stored
values,[@maleczek; @pasma2021] and no reference standard for arterial artefact is
agreed.[@bergmann] Our approach uses the waveform only to decide whether a monitor value can be
trusted, and can be reproduced on any dataset that stores both.

## Implications

Investigators should use a per-minute median with a range filter, or a rule such as F3, report
resolution as carefully as threshold, and avoid running-median smoothing and unfiltered area-
or time-weighted exposures below 55 mmHg. Paired multiverse comparisons should check the
coverage of their intervals before unblinding: here, percentile intervals covered the truth in
half of null datasets.

The episode probabilities are retrospective and describe a population. They must not be used to
delay treatment: a sudden fall should be treated as real until the waveform shows otherwise. At 10 s, one in five falls to 20–39 mmHg was not
flagged, and one in five flagged deep episodes had a low cuff pressure within a minute. An
automated system could use such probabilities to *annotate* a probable artefact, never to
*suppress* an alarm; a simple drop rule does not separate deep artefacts from deep real events
(specificity 0.07 below 40 mmHg). Where possible, the cuff should be placed on the limb
opposite an arterial line,[@saugel] and it remains an essential cross-check of the line.

## Strengths and limitations

The reference comes from the waveform recorded alongside the numbers and never replaces monitor
values; the protocol was frozen after a permuted dry run, and all data and code are public.

Limitations:
- **The equivalence verdict rests on few patients** (33 discordant) and would not have survived
  two AKI cases among them. It may not transfer to cohorts with more artefact or a stronger
  association.
- **No human rater adjudicated the reference.** The AI rater shares its model family with the
  classifier's designer; a 400-snippet set with a hidden key is released for human raters.
- **The reference is waveform-screened, not error-free.** The classifier cannot see levelling
  errors and zero drift (about 7 mmHg per 10 cm), most over-damping, partial occlusion or very
  short flushes, and 28% of deep "physiological" episodes had a cuff MAP ≥ 70 mmHg nearby.
- **AKI was defined by creatinine alone**, without urine output; postoperative creatinine
  testing varied by department, and end-tidal carbon dioxide and vasopressor data were not
  examined around deep episodes.
- **Much post-induction hypotension was missed**, because monitoring started a median of 10 min
  after the start of anaesthesia.[@sudfeld]
- **One centre, few events** (2016–2017, mainly general and thoracic surgery, 3.6% AKI), with
  adjusted odds ratios that depend on adjustment for anaesthesia duration. Charted resolutions
  were simulated, not taken from real records,[@kool] and artefact frequencies depend on local
  practice, although the mechanisms should transfer.
