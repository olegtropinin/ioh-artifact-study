# Introduction

Intraoperative hypotension is associated with acute kidney injury (AKI), myocardial injury and
death.[@walsh; @salmasi; @sun; @wesselink] Thresholds derived from these studies, typically a
mean arterial pressure (MAP) below 65 mmHg for more than a few minutes, now appear in consensus
statements and quality metrics.[@poqi] Almost all of this evidence comes from retrospective
analyses of numbers stored by anaesthesia information management systems. These are one value
per minute or less, taken from the monitor rather than from the waveform the clinician sees.

Invasive arterial pressure is the reference standard of these studies, yet the stored numbers
inherit every event that disturbs an arterial line: flushing, blood sampling through a
stopcock, zeroing, a kinked or damped catheter and cuff inflation on the same
limb.[@kool; @pasma2021; @gardner; @saugel] Choosing among published artefact filters changes
the measured incidence of hypotension up to twofold but the association with myocardial injury
little;[@pasma2020] coarser sampling inflates the measured burden of hypotension against a
waveform reference, although its effect on outcome associations has only been
extrapolated;[@jacobsson] and how hypotension is modelled changes the estimated odds
ratios.[@vernooij]

Recent studies of the open VitalDB dataset relating arterial pressure to kidney injury applied
a single cleaning rule or did not describe one.[@leesb; @ensarioglu; @folks]

Four questions remain open. How much of recorded hypotension is artefact when artefacts are
identified from the waveform? Do the artefact rule and the data resolution change the
association between hypotension and AKI when it is estimated directly? Is misclassification
*differential*: arterial blood is sampled more often in sicker patients, and if sampling
artefact were recorded as hypotension preferentially in patients who later develop AKI, it
would bias associations away from the null? And which recorded low-pressure episodes are
artefact, and how quickly can this be recognised?

We used the two parallel recordings in VitalDB, the 500 Hz waveform and the monitor's 2-s
numbers, to build a waveform-referenced MAP series. We compared it with 420 pipelines that a
retrospective study could plausibly use, in a pre-specified multiverse
analysis.[@steegen; @simonsohn]
