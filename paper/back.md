## Conclusions

Arterial-line artefacts are frequent events but a small part of recorded hypotension. With
per-minute medians and a simple range filter, they do not bias the association between
≥ 10 min of MAP < 65 mmHg and AKI, and they are not recorded preferentially in patients who
develop AKI. Investigators should avoid running-median smoothing and unfiltered
depth-weighted exposures, and should report resolution as carefully as thresholds.
Clinicians and automated systems should treat a brief, very deep fall in recorded pressure as
probable artefact until the waveform says otherwise. The cuff should be placed on the
arm opposite an arterial line where possible.

# Declarations

**Ethics.** This is a secondary analysis of the de-identified, publicly released VitalDB
dataset. Collection of the data was approved by the institutional review board of Seoul
National University Hospital, as described in the data descriptor.[@vitaldb] No further
approval or consent was required.

**Funding.** None.

**Competing interests.** None declared.

**Data and code availability.** VitalDB is openly available at https://vitaldb.net. The
analysis code, the frozen protocol with all amendments, the permuted dry run, aggregate
results and the 400-snippet adjudication set are available at [REPOSITORY URL]. The
adjudication key is available from the author on request, to preserve blinding of future
raters.

**Use of artificial intelligence.** The author used an AI system (Claude, Anthropic) for
substantial parts of this work, under the author's direction:
- writing the analysis code;
- an adversarial review of the methods before the protocol was frozen;
- drafting the manuscript.

An instance of the same AI system was also used as the blinded secondary rater of waveform
snippets, as described in the Methods. The author checked the code, outputs and text, and
takes full responsibility for the content. The AI system is not an author.

**Author contribution.** O.T. conceived and designed the study, performed the analysis,
interpreted the results and wrote the manuscript.

**Acknowledgements.** The author thanks the VitalDB team at Seoul National University
Hospital for making the dataset openly available.

# Figure legends

**Figure 1.** Examples of recorded hypotension that is artefact. Each panel shows the 500 Hz
arterial waveform (grey) and the lag-aligned 2-s monitor MAP (orange) around the start of a
recorded MAP < 65 mmHg (time 0). Shaded windows are labelled artefact or guard by the
classifier. The panels show, from top to bottom:
- transducer open to air (zeroing);
- closed stopcock during blood sampling;
- fast flush followed by recovery;
- a non-pulsatile trace with a cuff reading within 3 min.

**Figure 2.** Arterial artefact around non-invasive cuff measurements. The percentage of 2-s
arterial windows labelled artefact is plotted against time relative to the moment a new cuff
value appears (15,643 readings with a complete window).

**Figure 3.** Spurious minutes among recorded minutes with MAP < 65 mmHg, by filter
(F0–F6) and resolution (2-s, one value per minute, 1-min median). Orange bars show spurious
minutes (reference ≥ 65 mmHg), with patient-cluster bootstrap 95% CIs. Blue bars show
indeterminate minutes (no valid reference), which were never counted as artefact.

**Figure 4.** Probability that a recorded episode of MAP < 65 mmHg is waveform-flagged
artefact, by episode duration and nadir (106,725 episodes in 3,123 patients).

**Figure 5.** Ratio of odds ratios for AKI (≥ 10 min MAP < 65 mmHg) for every filter ×
resolution combination, each against the reference at the same resolution. Thin lines show
95% CIs (log ROR ± 1.96 × max(bootstrap SE, permutation-null SD)). Wide bands show
simultaneous 95% bands over the 35 cells. Grey shows the equivalence margin of 0.80–1.25.

**Figure 6.** Ratio of odds ratios at the 1-min median resolution by filter, exposure metric
and threshold. Orange cells: ROR < 1; blue cells: ROR > 1. AUC, area under the threshold; TWA, time-weighted average below the
threshold.

**Figure S1.** Flow of patients (see Results for counts).

**Figure S2.** Specification curve: ratios of odds ratios for all 420 pipeline
specifications, sorted. The lower panel marks the filter, resolution and threshold of each.
