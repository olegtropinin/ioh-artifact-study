# Arterial-line artefacts and intraoperative hypotension research (VitalDB)

Code for a pre-specified, waveform-referenced multiverse analysis of how arterial-line
artefacts and data-processing choices change (a) measured intraoperative hypotension and
(b) its estimated association with acute kidney injury.

Data: VitalDB open dataset (Lee HC et al., Sci Data 2022). Nothing patient-level is
redistributed here; every number is recomputed from the public API.

## Reproduce

Python 3.10.5; package versions in `requirements.txt`. VitalDB tables were downloaded on
2026-10-26; their SHA-256 sums are in `data_checksums.sha256` (the API serves the current
release, so check the sums). Waveform files are fetched per case through the `vitaldb`
package; 211 cases with a listed `SNUADC/ART` track returned no waveform on that date
(`docs/waveform_not_retrievable_caseids.txt`). `extract.py` skips existing `.npz` files, so
delete `data/cases/` after any change to the features.

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
mkdir -p data && cd data && for t in cases trks labs; do curl -s https://api.vitaldb.net/$t -o $t.csv.gz; done; cd ..
shasum -a 256 -c data_checksums.sha256
.venv/bin/python src/outcomes.py                # covariates, KDIGO AKI
.venv/bin/python src/extract.py                 # 2-s waveform features (~1.5 h, network-bound)
.venv/bin/python src/run_all.py                 # pipelines and reference per case
.venv/bin/python -m pytest -q tests             # unit tests on synthetic series
.venv/bin/python src/descriptive.py             # outcome-free analyses
.venv/bin/python src/precision.py               # pre-unblinding precision check (simulated outcome)
.venv/bin/python src/analysis.py permuted       # dry run on a permuted outcome
.venv/bin/python src/null_calibration.py        # A15 null calibration (decides the interval rule)
.venv/bin/python src/analysis.py real           # pre-specified analysis (frozen at tag protocol-freeze)
.venv/bin/python src/validate_v1.py             # injection-recovery (implementation check)
.venv/bin/python src/adjudication.py            # 400-snippet adjudication set
.venv/bin/python src/ai_rater_agreement.py      # needs the ratings in out/adjudication and the key
.venv/bin/python src/figures.py descriptive && .venv/bin/python src/figures.py real
.venv/bin/python src/tables.py real && .venv/bin/python paper/build.py
# post hoc (not pre-specified; see docs/protocol.md, "Notes after unblinding")
.venv/bin/python src/posthoc_depth.py
.venv/bin/python src/posthoc_cuff_site.py
.venv/bin/python src/posthoc_review.py
.venv/bin/python src/posthoc_models.py real
.venv/bin/python src/posthoc_stats.py
.venv/bin/python src/validate_v1_sweep.py
```

Thresholds of the window classifier (guard, noise, pulsatility) were set by inspection of
descriptive, outcome-free data during development (fewer than 600 cases, before the full
extraction); no script reproduces that tuning.

## Files

| Path | What |
|---|---|
| `docs/protocol.md` | analysis protocol with amendments, frozen at tag `protocol-freeze` |
| `docs/novelty_round1.md`, `docs/novelty_round2.md` | literature checks |
| `src/artifact.py` | 2-s waveform window classifier |
| `src/pipelines.py` | retrospective pipelines (filters × resolutions × metrics) and the reference |
| `src/models.py` | cohort, Firth logistic regression, splines |
| `src/analysis.py` | all outcome analyses |
| `out/adjudication/` | blinded snippets and blank rating form for human raters (the key is kept out of version control) |
| `docs/reviews/` | round-1 AI peer reviews and responses |
| `docs/ai_rater_prompt.md` | prompt and blinding conditions of the AI rater |
