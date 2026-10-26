# Round 1 — statistical reviewer and signal/reproducibility reviewer (AI agents), 2026-10-26

Both verdicts: major revision.

## Statistical reviewer — major
- S-M1 The ROR rests on the discordant patients (33 in the AKI set for F1 × R3); show the
  discordant × AKI table, expected count and an exact bound; translate into an ROR bound.
  (Checked: 28 up-flipped with 0 AKI, 5 down-flipped with 0 AKI.)
- S-M2 The A15 interval is validated only at ROR = 1; an equivalence claim needs operating
  characteristics at the margins (TOST): simulate with a covariate-conditional DGP at true
  ROR 1.25 and 0.80; compare permutation null with a parametric null; archive the calibrated
  coverage with permutations independent of those that estimated the SD; do not recommend
  permutation-only checking.
- S-M3 OR_ref is null (0.94); report OR_ref/OR_pipe with CIs and crude OR; the analysis tests
  differential, not non-differential, error; drop the attenuation factor.
- S-M4 Equivalence under simultaneous bands (19/35); borderline cells; the simultaneous
  critical value mixes bootstrap-standardised max-|z| with calibrated SE; report the
  pre-specified fragility summaries (CI excluding 1: 181/420; significance flips).
- S-M5 The TWA55 ROR 0.30 is the minimum of 420 and post hoc; base the depth-metric advice on
  measurement-level evidence; state 'R3 only'; mention 60 mmHg; do not compare per-mmHg with
  per-10-min ORs.
- S-M6 O5: per-SD scaling hides imprecision (per unit 0.59, 0.12–2.86); the interpreted
  version is not the primary pipeline; negative control in the same model and not null.
- S-M7 Pre-specified S4 (missing creatinine = no AKI) and S6 (include transplantation) were
  never run — silent deviation.
- S-M8 Use "waveform-flagged"/"waveform-referenced", not "artefact"/"verified" (A1).
- S-M9 EPV ≈ 4.5; add a disease-risk-score sensitivity; Wald vs profile CIs.
- Minor: 150 vs 152 snippets; 208,104 fits not 182,000; sens ≥ 0.99 false for F5×R4/R5;
  1.8–3.3% not 3.1%; 4–10× not 3–5×; "several cells" → one in real data; mortality n;
  first eligible case differs between cohorts; masked denominators; B per analysis; caps in
  Methods; "isolates waveform-based cleaning"; waveform-mean explanation; two baselines for
  the cuff profile; margin rationale; AF n = 13; covariate missingness; p_perm centring.

## Signal/reproducibility reviewer — major
- G-M1 Injection–recovery largely circular (injections sized to cross the classifier's own
  thresholds; clean segments pre-selected as valid; guard counted as detection); call it an
  implementation check; add amplitude/duration sweeps; report per intended label.
- G-M2 NIBP timing shifted by the arterial lag (pipelines.py:210, figures.py:142); the value
  is written at the end of the oscillometric cycle; split regular vs irregular readings;
  subtype breakdown; report the pedal/femoral negative control.
- G-M3 No check of monitor–waveform agreement inside valid windows; add a discordance label
  and a sensitivity analysis; explain the waveform-mean ROR.
- G-M4 Reference minute validity computed on the bridged series (interpolated values count as
  valid), unlike protocol §3; S3 therefore barely changes anything.
- G-M5 Equivalence nearly guaranteed by the small number of flips; report the attainable
  ROR range.
- G-M6 AI-rater agreement not reproducible from code; rater sees the waveform only; subset
  enriched to 43% artefact; state blinding conditions.
- Methods-vs-code mismatches: "radial" (no site filter); PP is p98−p02; guard30 is 6 s/30 s;
  O6 rule is not a tree; NIBP shifted; 152 snippets; "low-pressure" windows; patients vs
  cases in V1; fit count; mortality cohort requires eGFR; exposure caps; missing = 0.0.
- Reproducibility: README incomplete; versions unpinned; data not checksummed; non-retrievable
  case list not committed; no script for threshold calibration or the AI rating.
