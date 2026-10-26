# Discussion (outcome-independent parts; outcome paragraphs added after unblinding)

## Practical implications

**For investigators.**
- The per-minute median is robust. Combined with any range filter it leaves < 1% of
  hypotensive minutes spurious, and patient-level exposure categories agree with a
  waveform-verified reference at κ ≥ 0.97.
- Instantaneous per-minute sampling — the form in which many anaesthesia information
  management systems store values — carries 3–5 times more spurious hypotension, and range
  filters do not remove it.
- The 7-point running median, recommended in earlier work as a robust smoother, should not
  be used to estimate hypotension exposure. On per-minute data it creates spurious minutes
  and masks about a quarter of true hypotension. On charted 5- or 15-min data it erases
  most exposure.
- Resolution matters more than the filter: charting every 5 or 15 min raised the proportion
  of exposed patients from 42% to 51–53% against the same reference. Thresholds derived
  from charted records are therefore not transferable to high-resolution data, nor the
  reverse.

**For clinicians and automated systems.**
- A very short, very deep fall in recorded MAP is usually not hypotension. Of episodes
  lasting ≤ 60 s with a nadir < 40 mmHg, 65–90% were artefact. Episodes lasting more than a
  minute with a nadir ≥ 40 mmHg were artefact in ≤ 2%.
- A simple rule — a fall of more than 20 mmHg from the preceding 30-s maximum — identified
  nine of ten artefactual episodes while falsely flagging about one physiological episode in
  twelve. Its positive predictive value (0.46) is too low for it to suppress an alarm
  silently. It is better used to prompt a glance at the waveform before treating, and to
  clean data retrospectively.
- Cuff inflation is a frequent, avoidable source of arterial artefact. Artefact on the
  arterial trace was eight times more frequent in the minute before a cuff value appeared
  than at other times. It peaked 16 s before the value, at five times its baseline, which is
  the time course of an inflating cuff occluding the cannulated arm.
  Placing the cuff on the other arm, or suspending cuff cycling while an arterial line is
  working, would remove it. Some departments do this already; our data quantify why it
  matters. In retrospective studies that compare cuff and arterial pressure (for example
  studies of cuff–arterial discordance), arterial values from the minute before each cuff
  reading are enriched for artefact and should be treated with caution.

## Strengths

- To our knowledge, the first waveform-referenced multiverse analysis of intraoperative
  hypotension and AKI: every pipeline compared with a reference at matched resolution,
  rather than with another pipeline.
- The reference never replaces monitor values, so calibration differences between the
  monitor and the analogue-to-digital converter do not enter the comparison.
- Independent physiological checks of the reference (cuff pressure, ECG and
  plethysmographic pulse, atrial fibrillation), injection–recovery, and a pre-specified
  null calibration of the inferential method.
- Analysis protocol frozen after an end-to-end dry run on a permuted outcome. Every
  deviation from it is recorded with its reason and timing.
- All data are public and all code is released.

## Limitations

- **No human adjudication.** No human expert rated the reference. Its validity rests on
  physiological cross-checks, injection–recovery and an AI rater from the same model family
  that helped design the classifier, which is not independent. A 400-snippet adjudication
  set with a hidden key is released so that this gap can be closed by others.
- **Blind spots of morphology rules.** Over-damping was detected in only 12% of injections
  and a transducer offset not at all. Both preserve a pulsatile trace, so any
  morphology-based reference, ours included, will miss them. Over-damping lowers systolic
  but changes MAP little, which limits the consequence for MAP-based exposure.
- **Single centre.** One centre (Seoul National University Hospital, 2016–2017), mainly
  general and thoracic surgery, with few deaths and a low incidence of creatinine-defined
  AKI (3.6%). Precision for the AKI association itself is modest. Our contrast is a ratio
  of two estimates from the same patients, which is much more precise than either
  estimate.
- **Generalisability of artefact frequency.** Practice determines artefact frequency:
  sampling frequency, flushing, cuff placement and zeroing all vary by institution. The
  absolute figures will not transfer, but the mechanisms and the direction of the
  resolution and smoothing effects should.
- **Creatinine-only AKI.** AKI was defined by creatinine only, without urine output, and
  ascertainment depended on postoperative creatinine sampling. This was addressed in a
  sensitivity analysis but not eliminated.
- **Thresholds and outcome scope.** Thresholds were tuned on descriptive data before
  outcomes were examined. Two amendments (A14, A15) were made after the permuted dry run
  but before unblinding.
