## Conclusions

Arterial-line artefacts were frequent events but a small part of recorded hypotension. With
per-minute medians and a range filter, artefact handling did not detectably change the
association between hypotension and AKI. We found no evidence that artefact was recorded
preferentially in patients who developed AKI, although the equivalence verdict rested on few
discordant patients.

Running-median smoothing and unfiltered area-based exposures distort measured hypotension.
Brief, very deep recorded falls are often artefact in retrospect, but a sudden fall should
prompt a look at the waveform, never a delay in treatment.

# Declarations

**Ethics.** This is a secondary analysis of the de-identified, publicly released VitalDB
dataset. The acquisition and public release of the data were approved by the Institutional
Review Board of Seoul National University Hospital (H-1408-101-605), which waived written
informed consent because the data are anonymous.[@vitaldb] No further ethics approval or
consent was required for this analysis.

**Funding.** None.

**Competing interests.** None declared.

**Data and code availability.** VitalDB is openly available at https://vitaldb.net. The
analysis code, the frozen protocol with all amendments, the permuted dry run, aggregate
results and the 400-snippet adjudication set are available at
https://github.com/olegtropinin/ioh-artifact-study (archived at Zenodo,
https://doi.org/10.5281/zenodo.23726000). The
adjudication key is available from the author on request, to preserve blinding of future
raters.

**Use of artificial intelligence.** The author used an AI system (Claude Opus 5.5, Anthropic) for
substantial parts of this work, under the author's direction:
- writing the analysis code;
- an adversarial review of the methods before the protocol was frozen;
- three simulated peer reviews of the draft (statistical, clinical, signal processing), which
  led to the post-unblinding changes listed in the Supplementary Protocol;
- drafting the manuscript.

An instance of the same AI system was also used as the blinded secondary rater of waveform
snippets, as described in the Methods. The author checked the code, outputs and text, and
takes full responsibility for the content. The AI system is not an author.

**Author contribution.** O.T. conceived and designed the study, performed the analysis,
interpreted the results and wrote the manuscript.

**Acknowledgements.** The author thanks the VitalDB team at Seoul National University
Hospital for making the dataset openly available.

# Figure legends

**Figure 1.** Recorded hypotension that is waveform-flagged artefact. Each panel shows the
500 Hz arterial waveform (grey) and the lag-aligned 2-s monitor MAP (orange) around the start
of a recorded MAP below 65 mmHg (time 0). Shaded windows are labelled artefact or guard. From
top to bottom:
- a transducer open to air (zeroing);
- a stopcock turned off to the patient during blood sampling;
- a fast flush followed by recovery;
- a non-pulsatile trace with a cuff reading within 3 min.

**Figure 2.** Arterial artefact around non-invasive cuff measurements, by artefact type. The
plot shows the percentage of 2-s arterial windows with each label, by time relative to the
moment a new cuff value appears (14,307 readings with a complete −300 to +30 s window).

**Figure 3.** Spurious minutes among recorded minutes with MAP below 65 mmHg, by filter and
resolution: R1, 2-s stream; R2, one value per minute; R3, 1-min median. Orange: spurious
(reference ≥ 65 mmHg), with patient-cluster bootstrap 95% CI. Blue: indeterminate (no valid
reference), never counted as artefact.

**Figure 4.** Ratio of odds ratios for AKI (≥ 10 min below 65 mmHg) for every filter ×
resolution combination, each against the reference at the same resolution.
- Points: ratio of odds ratios.
- Thin lines: 95% CI, log ROR ± 1.96 × max(bootstrap SE, permutation-null SD).
- Wide bands: simultaneous 95% bands over 35 cells.
- Grey: equivalence margin 0.80–1.25.

**Figure S1.** Flow of patients.

**Figure S2.** Specification curve: ratios of odds ratios for all 420 pipeline
specifications, sorted. The lower panel marks the filter, resolution and threshold.

**Figure S3.** Probability that a recorded episode is waveform-flagged, by final duration and
nadir (the data of Table 2).

**Figure S4.** Ratio of odds ratios at the 1-min median resolution by filter, exposure metric
and threshold (post hoc display). Orange: ROR < 1; blue: ROR > 1.
