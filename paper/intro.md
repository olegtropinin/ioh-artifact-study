# Introduction

Intraoperative hypotension is associated with acute kidney injury, myocardial injury and
death, and thresholds derived from such studies — typically a mean arterial pressure (MAP)
below 65 mmHg for more than a few minutes — now appear in consensus statements and drive
quality metrics, trials and automated decision support.^13–15^ Almost all of this evidence
comes from retrospective analyses of numbers stored by anaesthesia information management
systems: one value per minute or less, taken from the monitor rather than from the
waveform the clinician sees.

Invasive arterial pressure is the reference standard of these studies, but the stored
numbers inherit every event that disturbs an arterial line: flushing, blood sampling,
transducer zeroing, a closed stopcock, a kinked catheter, and cuff inflation on the same
limb.^16,17^ Earlier work established three things. Choosing among published artefact
filters changes the measured incidence of hypotension up to twofold, yet changed the
association with myocardial injury little.^9^ Coarser sampling inflates the measured
burden of hypotension against a waveform reference, although its effect on outcome
associations has only been extrapolated.^7^ And how hypotension is modelled changes the
estimated odds ratios.^18^ Recent studies of the open VitalDB dataset relating
intraoperative arterial pressure to kidney injury applied a single cleaning rule or did
not describe one, and none examined its influence.^5,19,20^

Three questions therefore remain open. First, when artefacts are identified from the
waveform itself rather than from rules applied to the numbers, how much of recorded
hypotension is artefact? Second, does the combination of artefact rule and data resolution
change the estimated association between hypotension and acute kidney injury when that
association is estimated directly, rather than extrapolated? Third — and not, to our
knowledge, previously examined — is artefact misclassification *differential*? Arterial
blood is sampled more often in sicker and less stable patients; if sampling artefacts are
recorded as hypotension preferentially in patients who later develop kidney injury, the
error would bias published associations away from, not towards, the null.

We used the two parallel recordings in VitalDB — the 500 Hz waveform and the monitor's 2-s
numerics — to build a waveform-referenced MAP series, and compared it with 420 pipelines
that a retrospective study could plausibly use, in a pre-specified multiverse
(specification-curve) analysis.^21,22^
