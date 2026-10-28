Oleg Tropynin
Independent researcher, Karaganda, Kazakhstan
ORCID 0009-0006-5431-4285 · tropininoleg@gmail.com

The Editor-in-Chief
Journal of Anesthesia

Dear Editor,

I submit the Original Article "How much recorded intraoperative hypotension is arterial-line
artefact, and does it bias the association with creatinine-defined acute kidney injury? A
waveform-referenced cohort study" for consideration in the Journal of Anesthesia.

Thresholds for intraoperative hypotension come largely from retrospective analyses of
monitor numbers that inherit every flush, blood sample, zeroing and cuff inflation on the
arterial line. Earlier studies compared artefact filters with one another or extrapolated
their effect on outcomes. Using the open VitalDB dataset, we instead labelled each 2-s monitor
value from the simultaneously recorded 500 Hz arterial waveform and compared that
waveform-referenced series with 420 retrospective processing pipelines in 3,249 patients.

The main findings are:
- With a per-minute median and a range filter, 0.7% of recorded hypotensive minutes were
  spurious against the waveform reference, and the ratio of adjusted odds ratios for AKI was
  0.96 (0.86–1.06), within a pre-specified equivalence margin. We report openly that this
  verdict is fragile: two AKI cases among the 28 reclassified patients would have made it
  inconclusive.
- Running-median smoothing and unfiltered area-based exposures distort measured hypotension,
  and resolution changes the share of exposed patients by a fifth.
- Arterial artefact rises sixfold during the non-invasive cuff cycle, mostly as a
  non-pulsatile trace; we present arm occlusion as a hypothesis, not a finding.

The analysis protocol was frozen in a tagged git commit after a full dry run on a permuted
outcome, before any exposure–outcome association was computed; every later change is listed
with its date and reason in Online Resource 1. Code, protocol, aggregate results and a blinded
400-snippet adjudication set are public (https://doi.org/10.5281/zenodo.23726000).

As required by the journal, the use of a large language model (Claude Opus 5.5, Anthropic) is
described in the Methods and in the declarations: it wrote analysis code, reviewed the methods,
simulated peer review, drafted text and served as a secondary blinded rater, under my direction.
I checked all code, outputs and text and take full responsibility for the content. The AI system
is not an author.

The manuscript has 3,994 words of main text, a 250-word structured abstract, 3 tables, 4 figures
and 32 references; supplementary material is in Online Resource 1. Colour figures are requested for
the online version only. The work has not been
published and is not under consideration elsewhere; the manuscript and code are archived in a
public repository (GitHub/Zenodo), which is not a journal publication. There was no funding and
I have no competing interests. The study used only de-identified public data whose collection
and release were approved by the Institutional Review Board of Seoul National University
Hospital (H-1408-101-605).

Thank you for considering this manuscript.

Yours sincerely,

Oleg Tropynin
