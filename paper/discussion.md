# Discussion

## Principal findings

In 3,249 patients with a high-resolution arterial waveform, artefacts were frequent events but
a small part of recorded hypotension. With the processing most retrospective studies use, a
per-minute median and a range filter, fewer than 1% of hypotensive minutes were spurious. The
exposure category changed in 1.2% of patients.

Two features of the cohort define what our main result can and cannot say:
- **The canonical exposure was not associated with AKI after adjustment.** For ≥ 10 min below
  65 mmHg the adjusted odds ratio was 0.94, although the crude odds ratio was 1.65.
- **Non-differential error had almost nothing to act on.** When the reference association is
  null, non-differential misclassification cannot attenuate it. The equivalence of the
  pipeline and the reference (ROR 0.96) therefore tests mainly *differential* error, the
  scenario in which artefact recorded preferentially in patients destined for AKI would
  manufacture an association.

That scenario was not present:
- the 33 patients whose category changed included no AKI case;
- spurious hypotension was unrelated to blood sampling and to AKI;
- the equivalence verdict held under every sensitivity analysis, including the two
  pre-specified analyses we initially omitted.

Where an association was present (55 mmHg, and the slope per 10 min), the pipeline estimates
were close to the reference but too imprecise to establish equivalence.

Three processing choices mattered more than the filter did:
- **The 7-point running median** created spurious hypotension and masked a fifth of true
  hypotension. On charted data it erased most exposure.
- **Unfiltered area-based exposures below 55 mmHg** were dominated by zero and flush values in a
  few patients: over a third of the area was artefact.
- **Resolution** classified a fifth more patients as exposed, without a detectable change in the
  odds ratio.

## Comparison with previous work

**Filters and resolution.** Pasma et al. compared eight filters on per-minute data. The filter
changed the measured incidence of hypotension up to twofold but changed the association with
myocardial injury little.[@pasma2020] Jacobsson et al. showed, against a waveform reference,
that coarse sampling inflates measured hypotension, and extrapolated an effect on
outcomes.[@jacobsson] Our study adds three things:
- an external, waveform-referenced comparator at every resolution;
- a direct estimate of the outcome effect, with a pre-specified equivalence criterion;
- a test for differential error.

We agree with both studies on duration-based exposures. Unlike Pasma et al., we found that the
7-point median distorts exposure substantially, even where the ratio of odds ratios happened
to stay near 1. The AWAKE trial showed that continuous arterial monitoring changes the
*measured* and *treated* hypotension at induction.[@kouz] Our resolution results are the
retrospective counterpart: the same patients look different at different sampling rates.

**Cuff and arterial pressure.** Wax et al.,[@wax] and more recently a preprint from the MOVER
cohort,[@liu] treated disagreement between cuff and arterial pressure as clinical information.
We found a measurement mechanism that generates such disagreement: arterial artefact rose
sixfold during the cuff cycle, mostly as a non-pulsatile trace. Several features point to
occlusion of the cannulated arm in a subset of patients:
- the excess was larger with radial than with lower-limb catheters;
- it was larger on the right than on the left;
- it was present at regularly cycled readings;
- flush labels barely rose.

It was not the whole story. A smaller excess with pedal and femoral catheters suggests other
activity around cuff cycles, such as handling of the arm or the line. Studies of discordance
should exclude arterial values from the cuff cycle, or show that their results survive that
exclusion.

**Artefact detection.** Earlier work compared algorithmic and machine-learning detection with
human annotation of stored values,[@maleczek; @pasma2021] and a scoping review found no
agreed reference for arterial artefact.[@bergmann] Our classifier uses the waveform only to
decide whether a monitor value can be trusted. It can be reproduced on any dataset that
stores both.

## Implications

**For investigators:**
- Use a per-minute median with a range filter, or a rule such as F3. Report the resolution as
  carefully as the threshold.
- Do not use running-median smoothing to estimate exposure.
- Do not compute area- or time-weighted exposures below 55 mmHg from unfiltered data.
- In paired multiverse comparisons, check the operating characteristics of the intervals
  before unblinding, at the null and at the decision margins. Permutation alone checks only
  the null. Without this check, our percentile intervals would have covered the truth in half
  of null datasets.

**For clinicians and alarm design:**
- Most very brief, very deep recorded falls proved to be artefact in retrospect. Within the
  first 10–30 s, a fall to 20–39 mmHg was artefact more often than not. By 60 s, more than
  nine in ten were real.
- A fall below 20 mmHg remained artefact in a third of cases even after 2 min.
- These are retrospective probabilities. They do not justify delaying treatment. A sudden fall
  should prompt an immediate look at the arterial waveform, the plethysmograph and end-tidal
  carbon dioxide.
- A system could use them to *annotate* a probable artefact, never to *suppress* an alarm. The
  simple drop rule we derived cannot even separate deep artefacts from deep real events
  (specificity 0.07 below 40 mmHg).
- Where possible, place the cuff on the limb opposite an arterial line, consistent with
  standard guidance on arterial pressure measurement.[@saugel]

## Strengths and limitations

**Strengths:**
- The reference comes from the waveform recorded alongside the numbers, and it never replaces
  monitor values.
- The protocol was frozen after a permuted dry run. Every later change is documented.
- The validity of the reference was checked against independent signals: cuff pressure,
  pulse oximetry and ECG.
- The data are public and the code is released.

**Limitations:**
- **No human rater adjudicated the reference.** The AI rater shares its model family with the
  classifier's designer and sees only the waveform. A 400-snippet set with a hidden key is
  released for human adjudication, and it should show the monitor value as well as the
  waveform.
- **The classifier cannot see some important errors.** These are:
  - levelling errors and zero drift (about 7 mmHg per 10 cm, which matters in lateral and
    tilted positions);
  - most over-damping;
  - partial occlusion;
  - very short flushes.

  Our reference is therefore *waveform-screened*, not error-free.
- **The monitoring period started a median of 10 min after the start of anaesthesia.** It
  therefore missed most post-induction hypotension,[@sudfeld] which limits comparison with
  studies that use cuff values from induction onwards.
- **Single centre.** The data come from one centre in 2016–2017, mainly general and thoracic
  surgery, with a low incidence of creatinine-defined AKI (3.6%).
- **AKI ascertainment.** AKI was ascertained from creatinine only, without urine output, and
  depended on postoperative testing, which varied by department. Haemodilution may have hidden
  some AKI.
- **Few events.** With 91 events, the precision of each odds ratio is modest. The ratio of two
  estimates in the same patients is far more precise, but our equivalence result rests on few
  discordant patients and may not transfer to cohorts with more artefact or a stronger
  association.
- **Charting was simulated.** Simulated charting is a random sample of monitor values, not the
  selective charting of real records.[@kool]
- **Practice-dependent frequencies.** Artefact frequencies depend on local practice, so the
  absolute numbers will not transfer. The mechanisms and the direction of the resolution and
  smoothing effects should.
