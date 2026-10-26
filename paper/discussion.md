# Discussion

## Principal findings

In 3,249 patients with a high-resolution arterial waveform, artefacts were frequent events
but a small fraction of recorded hypotension. With the processing most retrospective studies
use — a per-minute median and a simple range filter — fewer than 1% of hypotensive minutes
were spurious, and the association between ≥ 10 min of MAP < 65 mmHg and AKI was the same
whether it was estimated from the monitor numbers or from a waveform-verified reference (ROR
0.96, 95% CI 0.86–1.06; pre-specified verdict: equivalent). No filter–resolution combination
moved the association beyond what chance allows. Artefactual hypotension was not recorded
preferentially in patients who later developed AKI, so the differential bias we set out to
test was not present.

Three choices did matter:
- **The 7-point running median.** It created and masked hypotension. On charted data it
  erased most exposure, and it produced the least stable associations.
- **Unfiltered depth-weighted exposures below 55 mmHg.** Areas and time-weighted averages
  below 55 mmHg are dominated by a few zero and flush values. The point estimates suggested
  a large dilution of the association (ROR 0.30 for the time-weighted average), though the
  post hoc interval was wide.
- **Resolution.** Charting every 5–15 min classified about a fifth more patients as exposed
  without changing the odds ratio.

At the level of individual episodes the picture differs from the cohort level. A recorded
fall below 40 mmHg lasting under a minute was artefact in most cases, whereas sustained
episodes were almost never artefact.

## Comparison with previous work

**Pasma et al.**[@pasma2020] applied eight filters to per-minute data. The filter changed the
measured incidence of hypotension up to twofold but changed the association with myocardial
injury little. Their comparison was between filters; ours was against an external
waveform-verified reference, across resolutions and exposure metrics, with an equivalence
criterion and a test for differential error. The two studies agree on duration-based
exposure and on the per-minute median, and they disagree on the 7-point median. Pasma et al.
included it among their filters. We found that it distorts exposure substantially even when
the ratio of odds ratios happens to stay near 1.

**Jacobsson et al.**[@jacobsson] showed against a waveform reference that coarse sampling
inflates measured hypotension, and they extrapolated an effect on outcome associations. We
reproduced the inflation (42% to 53% exposed) but could not detect the outcome effect. The
odds ratios with 5- and 15-min charting were within 10% of those at 1-min resolution, with
intervals that included both no effect and moderate effects.

**Cuff and arterial pressure.** Wax et al.[@wax] and, recently, a preprint of a MOVER cohort
study of cuff–arterial discordance[@liu] interpreted disagreement between cuff and arterial pressure
as clinical information. Our observation that arterial artefact rises eightfold in the minute
before a cuff reading identifies a measurement mechanism that generates exactly such
discordance, and is partly explained by occlusion of the cannulated arm. Studies of discordance should
exclude arterial values from the minute before each cuff reading, or show that their results
survive that exclusion.

**Artefact detection.** Earlier work compared algorithmic and machine-learning artefact
detection in anaesthesia records against human annotation.[@maleczek; @pasma2021] A recent
scoping review found no agreed reference for arterial artefact.[@bergmann] Our classifier
uses the waveform only to decide whether a monitor value is trustworthy. This sidesteps
calibration differences between monitor and waveform and can be reproduced on any dataset
that stores both.

## A methodological lesson

The usual percentile bootstrap interval for a difference between two estimates from the same
patients was badly anti-conservative here. Under a permuted outcome it covered the true value
in only half of the trials for the primary contrast. The reason is structural: when two
exposure definitions disagree in a few dozen patients, the bootstrap distribution of their
contrast is spiky and its central 95% is too narrow. Multiverse and specification-curve
analyses routinely compare highly correlated specifications in exactly this way. Without the
null calibration, which we pre-specified only after it surfaced in the dry run, several cells
in this study would have been reported as significant differences that do not exist. We
recommend that such analyses check their intervals against permuted outcomes before
unblinding.
