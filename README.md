# Arterial-line artefacts and intraoperative hypotension research (VitalDB)

Code for a pre-specified, waveform-referenced multiverse analysis of how arterial-line
artefacts and data-processing choices change (a) measured intraoperative hypotension and
(b) its estimated association with acute kidney injury.

Data: VitalDB open dataset (Lee HC et al., Sci Data 2022). Nothing patient-level is
redistributed here; every number is recomputed from the public API.

## Reproduce

```bash
python3 -m venv .venv && .venv/bin/pip install numpy scipy pandas matplotlib statsmodels vitaldb pytest
mkdir -p data && cd data && for t in cases trks labs; do curl -s https://api.vitaldb.net/$t -o $t.csv.gz; done; cd ..
.venv/bin/python src/outcomes.py                # covariates, KDIGO AKI
.venv/bin/python src/extract.py                 # 2-s waveform features (~1.5 h, network-bound)
.venv/bin/python src/run_all.py                 # pipelines and reference per case
.venv/bin/python -m pytest -q tests             # unit tests on synthetic series
.venv/bin/python src/descriptive.py             # outcome-free analyses
.venv/bin/python src/precision.py               # pre-unblinding precision check (simulated outcome)
.venv/bin/python src/analysis.py permuted       # dry run on a permuted outcome
.venv/bin/python src/analysis.py real           # pre-specified analysis
.venv/bin/python src/validate_v1.py             # injection-recovery
.venv/bin/python src/adjudication.py            # 400-snippet adjudication set
.venv/bin/python src/figures.py descriptive && .venv/bin/python src/figures.py real
```

## Files

| Path | What |
|---|---|
| `docs/protocol.md` | analysis protocol with amendments, frozen at tag `protocol-freeze` |
| `docs/novelty_round1.md`, `docs/novelty_round2.md` | literature checks |
| `src/artifact.py` | 2-s waveform window classifier |
| `src/pipelines.py` | retrospective pipelines (filters × resolutions × metrics) and the reference |
| `src/models.py` | cohort, Firth logistic regression, splines |
| `src/analysis.py` | all outcome analyses |
| `out/adjudication/` | blinded snippets, hidden key, blank rating form for human raters |
