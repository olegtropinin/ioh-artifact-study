## Table 1. Patient characteristics

| Characteristic | Descriptive cohort | AKI set: no AKI | AKI set: AKI |
|---|---|---|---|
| n | 3249 | 2472 | 91 |
| Age, years | 61 (51–69) | 62 (54–70) | 63 (56–72) |
| Female | 1444 (44.4) | 1053 (42.6) | 19 (20.9) |
| BMI, kg m⁻² | 23.0 (20.8–25.2) | 23.1 (20.9–25.2) | 22.6 (20.4–26.0) |
| ASA physical status ≥ 3 | 492 (15.1) | 283 (11.4) | 28 (30.8) |
| Emergency surgery | 413 (12.7) | 266 (10.8) | 19 (20.9) |
| Hypertension | 1085 (33.4) | 835 (33.8) | 42 (46.2) |
| Diabetes | 398 (12.2) | 318 (12.9) | 18 (19.8) |
| Baseline eGFR, mL min⁻¹ 1.73 m⁻² | 95 (82–104) | 95 (83–103) | 94 (74–104) |
| Preoperative haemoglobin, g dL⁻¹ | 13.0 (11.6–14.2) | 13.1 (11.8–14.3) | 11.7 (10.4–13.6) |
| General surgery | 2017 (62.1) | 1430 (57.8) | 67 (73.6) |
| Thoracic surgery | 1001 (30.8) | 943 (38.1) | 17 (18.7) |
| Gynaecology / urology | 231 (7.1) | 99 (4.0) | 7 (7.7) |
| Open approach | 1318 (40.6) | 908 (36.7) | 61 (67.0) |
| Anaesthesia duration, h | 3.8 (2.8–5.2) | 3.8 (2.8–4.9) | 4.3 (3.2–6.3) |
| Monitored time, min | 193 (134–272) | 188 (135–258) | 223 (157–346) |
| Reference minutes MAP < 65 mmHg | 7 (1–19) | 7 (1–18) | 11 (4–39) |
| Reference ≥ 10 min MAP < 65 mmHg | 1377 (42.4) | 1021 (41.3) | 49 (53.8) |

Values are median (IQR) or n (%). Reference = waveform-verified monitor MAP, 1-min median.

## Table 2. Probability that a recorded low-MAP episode is waveform-flagged artefact

| Nadir \ duration | <=10 s | 11-30 s | 31-60 s | 1-2 min | 2-5 min | >5 min |
|---|---|---|---|---|---|---|
| <20 mmHg | 79% (77–81); n = 1569 | 77% (74–80); n = 905 | 65% (58–71); n = 201 | 43% (34–52); n = 122 | 23% (16–31); n = 150 | 11% (4–21); n = 116 |
| 20-39 mmHg | 67% (64–70); n = 755 | 90% (89–92); n = 1813 | 75% (70–80); n = 386 | 12% (6–18); n = 125 | 1% (0–3); n = 232 | 4% (1–6); n = 248 |
| 40-54 mmHg | 59% (56–63); n = 1391 | 65% (61–69); n = 1508 | 13% (10–16); n = 661 | 2% (1–4); n = 903 | 1% (0–1); n = 1578 | 1% (0–2); n = 1177 |
| 55-64 mmHg | 2% (2–3); n = 66981 | 1% (1–2); n = 13525 | 1% (0–2); n = 5286 | 1% (0–2); n = 3346 | 0% (0–1); n = 2867 | 1% (0–1); n = 880 |

Episode: contiguous run of monitor MAP < 65 mmHg. Percent flagged (patient-cluster bootstrap 95% CI); n = episodes.

## Table 3. Every filter × resolution: measurement error and its effect on the AKI association

| Filter | Resolution | Spurious % of low minutes | Masked % | Exposed, pipeline / reference % | κ | ROR (95% CI) | Simultaneous band |
|---|---|---|---|---|---|---|---|
| F0 none | 2-s stream | 2.3 | 1.0 | 44.1 / 42.3 | 0.96 | 1.12 (0.92–1.36) | 0.82–1.54 |
| F0 none | 1 value/min | 3.4 | 1.8 | 46.5 / 44.5 | 0.95 | 1.06 (0.89–1.25) | 0.80–1.39 |
| F0 none | 1-min median | 0.8 | 1.3 | 43.4 / 42.4 | 0.97 | 0.99 (0.88–1.11) | 0.82–1.20 |
| F0 none | 5-min chart | – | – | 53.1 / 51.2 | 0.95 | 0.94 (0.86–1.04) | 0.81–1.10 |
| F0 none | 15-min chart | – | – | 54.4 / 53.2 | 0.96 | 0.99 (0.92–1.07) | 0.87–1.12 |
| F1 MAP 20–250 | 2-s stream | 2.0 | 0.8 | 43.7 / 42.3 | 0.96 | 1.09 (0.91–1.31) | 0.81–1.47 |
| F1 MAP 20–250 | 1 value/min | 3.3 | 1.8 | 46.3 / 44.5 | 0.96 | 1.06 (0.89–1.25) | 0.80–1.39 |
| F1 MAP 20–250 | 1-min median | 0.7 | 1.1 | 43.2 / 42.4 | 0.98 | 0.96 (0.86–1.06) | 0.80–1.14 |
| F1 MAP 20–250 | 5-min chart | – | – | 52.9 / 51.2 | 0.95 | 0.95 (0.87–1.03) | 0.82–1.09 |
| F1 MAP 20–250 | 15-min chart | – | – | 54.2 / 53.2 | 0.97 | 1.00 (0.93–1.08) | 0.88–1.13 |
| F2 MAP 30–200 | 2-s stream | 1.8 | 0.6 | 43.5 / 42.3 | 0.97 | 1.12 (0.94–1.34) | 0.83–1.50 |
| F2 MAP 30–200 | 1 value/min | 3.3 | 1.7 | 46.3 / 44.5 | 0.96 | 1.06 (0.90–1.25) | 0.81–1.39 |
| F2 MAP 30–200 | 1-min median | 0.5 | 0.9 | 43.0 / 42.4 | 0.98 | 0.97 (0.87–1.08) | 0.82–1.15 |
| F2 MAP 30–200 | 5-min chart | – | – | 53.0 / 51.2 | 0.95 | 0.94 (0.87–1.02) | 0.82–1.08 |
| F2 MAP 30–200 | 15-min chart | – | – | 54.3 / 53.2 | 0.97 | 1.01 (0.93–1.08) | 0.89–1.13 |
| F3 Jacobsson | 2-s stream | 0.6 | 0.4 | 42.5 / 42.3 | 0.98 | 1.05 (0.93–1.19) | 0.86–1.28 |
| F3 Jacobsson | 1 value/min | 3.1 | 1.6 | 46.1 / 44.5 | 0.96 | 1.07 (0.91–1.26) | 0.81–1.40 |
| F3 Jacobsson | 1-min median | 0.3 | 0.8 | 42.9 / 42.4 | 0.98 | 0.98 (0.89–1.08) | 0.83–1.15 |
| F3 Jacobsson | 5-min chart | – | – | 53.1 / 51.2 | 0.95 | 0.95 (0.88–1.03) | 0.83–1.08 |
| F3 Jacobsson | 15-min chart | – | – | 54.3 / 53.2 | 0.97 | 1.01 (0.94–1.09) | 0.90–1.14 |
| F4 consistency | 2-s stream | 0.9 | 0.6 | 42.8 / 42.3 | 0.98 | 1.03 (0.91–1.16) | 0.84–1.26 |
| F4 consistency | 1 value/min | 3.3 | 1.7 | 46.4 / 44.5 | 0.96 | 1.06 (0.89–1.25) | 0.80–1.39 |
| F4 consistency | 1-min median | 0.4 | 0.9 | 42.9 / 42.4 | 0.98 | 0.97 (0.88–1.07) | 0.82–1.14 |
| F4 consistency | 5-min chart | – | – | 53.3 / 51.2 | 0.95 | 0.94 (0.86–1.02) | 0.82–1.08 |
| F4 consistency | 15-min chart | – | – | 54.4 / 53.2 | 0.97 | 1.00 (0.93–1.08) | 0.89–1.13 |
| F5 F4 + neighbour | 2-s stream | 0.9 | 0.6 | 42.8 / 42.3 | 0.98 | 1.03 (0.91–1.16) | 0.84–1.26 |
| F5 F4 + neighbour | 1 value/min | 1.8 | 0.8 | 45.5 / 44.5 | 0.97 | 1.00 (0.83–1.20) | 0.74–1.34 |
| F5 F4 + neighbour | 1-min median | 0.3 | 0.7 | 42.8 / 42.4 | 0.98 | 0.97 (0.88–1.07) | 0.82–1.14 |
| F5 F4 + neighbour | 5-min chart | – | – | 51.8 / 51.2 | 0.96 | 0.95 (0.87–1.03) | 0.82–1.09 |
| F5 F4 + neighbour | 15-min chart | – | – | 52.1 / 53.2 | 0.95 | 1.03 (0.95–1.12) | 0.90–1.19 |
| F6 F4 + 7-pt median | 2-s stream | 3.0 | 3.5 | 42.4 / 42.3 | 0.98 | 0.99 (0.89–1.09) | 0.84–1.17 |
| F6 F4 + 7-pt median | 1 value/min | 9.9 | 24.0 | 36.1 / 44.5 | 0.82 | 1.13 (0.83–1.54) | 0.68–1.88 |
| F6 F4 + 7-pt median | 1-min median | 7.5 | 19.9 | 36.2 / 42.4 | 0.86 | 1.22 (0.92–1.61) | 0.77–1.92 |
| F6 F4 + 7-pt median | 5-min chart | – | – | 20.3 / 51.2 | 0.39 | 1.54 (0.97–2.44) | 0.72–3.28 |
| F6 F4 + 7-pt median | 15-min chart | – | – | 11.0 / 53.2 | 0.20 | 1.18 (0.67–2.07) | 0.46–2.99 |

Spurious: pipeline minute < 65 mmHg with reference ≥ 65. Masked: share of reference minutes < 65 that the pipeline records ≥ 65; neither is defined for charted resolutions. Exposure: ≥ 10 min with MAP < 65 mmHg; exposure prevalence and κ from the descriptive cohort (charted resolutions at phase offset 0). ROR (ratio of odds ratios, pipeline / reference at matched resolution) from the AKI set; 95% CI = log ROR ± 1.96 × max(paired-bootstrap SE, permutation-null SD); simultaneous band: bootstrap max-|z| critical value over all 35 cells applied to the same SE.
