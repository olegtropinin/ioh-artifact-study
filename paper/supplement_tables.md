# Supplementary tables

## Table S1. Recorded minutes with MAP < 65 mmHg classified against the reference (descriptive cohort)

| res | filter | low_min | spurious_frac | lo | hi | confirmed_frac | bridged_low_frac | indeterminate_frac | patients_with_spurious |
|---|---|---|---|---|---|---|---|---|---|
| R1 | F0 | 6.16e+04 | 0.023 | 0.021 | 0.025 | 0.932 | 0.012 | 0.032 | 2196 |
| R1 | F1 | 6.09e+04 | 0.020 | 0.019 | 0.022 | 0.943 | 0.012 | 0.025 | 2104 |
| R1 | F2 | 6.06e+04 | 0.018 | 0.017 | 0.020 | 0.947 | 0.011 | 0.024 | 2060 |
| R1 | F3 | 5.84e+04 | 0.006 | 0.005 | 0.006 | 0.974 | 0.008 | 0.012 | 1921 |
| R1 | F4 | 5.96e+04 | 0.009 | 0.008 | 0.009 | 0.963 | 0.009 | 0.020 | 2041 |
| R1 | F5 | 5.96e+04 | 0.009 | 0.008 | 0.009 | 0.963 | 0.009 | 0.020 | 2029 |
| R1 | F6 | 5.91e+04 | 0.030 | 0.028 | 0.032 | 0.942 | 0.010 | 0.019 | 2683 |
| R2 | F0 | 6.22e+04 | 0.034 | 0.031 | 0.037 | 0.934 | 0.019 | 0.013 | 1108 |
| R2 | F1 | 6.19e+04 | 0.033 | 0.030 | 0.036 | 0.938 | 0.019 | 0.010 | 1065 |
| R2 | F2 | 6.2e+04 | 0.033 | 0.030 | 0.036 | 0.938 | 0.020 | 0.010 | 1081 |
| R2 | F3 | 6.13e+04 | 0.031 | 0.029 | 0.034 | 0.946 | 0.019 | 0.004 | 1079 |
| R2 | F4 | 6.2e+04 | 0.033 | 0.030 | 0.036 | 0.938 | 0.020 | 0.009 | 1098 |
| R2 | F5 | 6.09e+04 | 0.018 | 0.017 | 0.020 | 0.953 | 0.019 | 0.009 | 754 |
| R2 | F6 | 5.15e+04 | 0.099 | 0.094 | 0.105 | 0.868 | 0.023 | 0.010 | 1338 |
| R3 | F0 | 5.96e+04 | 0.008 | 0.007 | 0.009 | 0.960 | 0.006 | 0.027 | 363 |
| R3 | F1 | 5.93e+04 | 0.007 | 0.006 | 0.007 | 0.964 | 0.006 | 0.023 | 311 |
| R3 | F2 | 5.94e+04 | 0.005 | 0.005 | 0.006 | 0.963 | 0.008 | 0.024 | 271 |
| R3 | F3 | 5.88e+04 | 0.003 | 0.003 | 0.004 | 0.970 | 0.009 | 0.018 | 170 |
| R3 | F4 | 5.92e+04 | 0.004 | 0.003 | 0.004 | 0.966 | 0.008 | 0.023 | 195 |
| R3 | F5 | 5.92e+04 | 0.003 | 0.003 | 0.004 | 0.967 | 0.008 | 0.022 | 177 |
| R3 | F6 | 5.19e+04 | 0.075 | 0.071 | 0.080 | 0.887 | 0.011 | 0.027 | 1105 |

low_min: pipeline minutes < 65; fractions are of low_min; lo/hi: patient-cluster bootstrap 95% CI of the spurious fraction.

## Table S2. Agreement of the binary exposure (≥ 10 min MAP < 65) with the reference (descriptive cohort)

| filter | res | prev_ref | prev_pipe | sens | spec | kappa | flips | up | down | mean_diff | loa_lo | loa_hi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F0 | R1 | 0.423 | 0.441 | 0.999 | 0.967 | 0.960 | 64 | 62 | 2 | 0.859 | -6.257 | 7.975 |
| F0 | R2 | 0.445 | 0.465 | 0.997 | 0.962 | 0.955 | 73 | 69 | 4 | 0.568 | -5.920 | 7.056 |
| F0 | R3 | 0.424 | 0.434 | 0.995 | 0.979 | 0.971 | 46 | 39 | 7 | 0.406 | -6.755 | 7.567 |
| F0 | R4 | 0.512 | 0.531 | 0.993 | 0.955 | 0.949 | 83 | 72 | 11 | 0.505 | -7.270 | 8.280 |
| F0 | R5 | 0.532 | 0.544 | 0.994 | 0.968 | 0.963 | 59 | 49 | 10 | 0.548 | -10.472 | 11.567 |
| F1 | R1 | 0.423 | 0.437 | 0.996 | 0.973 | 0.965 | 56 | 51 | 5 | 0.643 | -5.850 | 7.135 |
| F1 | R2 | 0.445 | 0.463 | 0.997 | 0.965 | 0.958 | 67 | 63 | 4 | 0.472 | -5.447 | 6.392 |
| F1 | R3 | 0.424 | 0.432 | 0.996 | 0.983 | 0.976 | 38 | 32 | 6 | 0.330 | -6.309 | 6.969 |
| F1 | R4 | 0.512 | 0.529 | 0.994 | 0.959 | 0.954 | 75 | 65 | 10 | 0.440 | -7.039 | 7.919 |
| F1 | R5 | 0.532 | 0.542 | 0.994 | 0.970 | 0.966 | 55 | 45 | 10 | 0.489 | -10.309 | 11.288 |
| F2 | R1 | 0.423 | 0.435 | 0.996 | 0.976 | 0.968 | 51 | 45 | 6 | 0.554 | -5.764 | 6.872 |
| F2 | R2 | 0.445 | 0.463 | 0.997 | 0.966 | 0.959 | 66 | 62 | 4 | 0.481 | -5.389 | 6.352 |
| F2 | R3 | 0.424 | 0.430 | 0.995 | 0.986 | 0.979 | 34 | 27 | 7 | 0.361 | -6.270 | 6.992 |
| F2 | R4 | 0.512 | 0.530 | 0.995 | 0.959 | 0.954 | 74 | 65 | 9 | 0.468 | -7.003 | 7.939 |
| F2 | R5 | 0.532 | 0.543 | 0.995 | 0.970 | 0.966 | 55 | 46 | 9 | 0.522 | -10.193 | 11.236 |
| F3 | R1 | 0.423 | 0.425 | 0.993 | 0.992 | 0.985 | 24 | 15 | 9 | -0.119 | -4.023 | 3.786 |
| F3 | R2 | 0.445 | 0.461 | 0.997 | 0.968 | 0.962 | 61 | 57 | 4 | 0.291 | -3.688 | 4.270 |
| F3 | R3 | 0.424 | 0.429 | 0.996 | 0.987 | 0.981 | 30 | 24 | 6 | 0.184 | -2.590 | 2.958 |
| F3 | R4 | 0.512 | 0.531 | 0.995 | 0.958 | 0.954 | 75 | 67 | 8 | 0.373 | -5.929 | 6.674 |
| F3 | R5 | 0.532 | 0.543 | 0.995 | 0.970 | 0.967 | 54 | 45 | 9 | 0.413 | -9.428 | 10.253 |
| F4 | R1 | 0.423 | 0.428 | 0.996 | 0.989 | 0.983 | 27 | 21 | 6 | 0.249 | -4.599 | 5.098 |
| F4 | R2 | 0.445 | 0.464 | 0.997 | 0.965 | 0.958 | 68 | 64 | 4 | 0.478 | -5.146 | 6.102 |
| F4 | R3 | 0.424 | 0.429 | 0.995 | 0.988 | 0.981 | 30 | 23 | 7 | 0.305 | -5.850 | 6.460 |
| F4 | R4 | 0.512 | 0.533 | 0.995 | 0.953 | 0.949 | 82 | 74 | 8 | 0.471 | -6.860 | 7.802 |
| F4 | R5 | 0.532 | 0.544 | 0.995 | 0.969 | 0.966 | 55 | 47 | 8 | 0.505 | -9.917 | 10.927 |
| F5 | R1 | 0.423 | 0.428 | 0.996 | 0.989 | 0.983 | 27 | 21 | 6 | 0.248 | -4.601 | 5.096 |
| F5 | R2 | 0.445 | 0.455 | 0.996 | 0.979 | 0.973 | 43 | 37 | 6 | 0.152 | -5.131 | 5.436 |
| F5 | R3 | 0.424 | 0.428 | 0.995 | 0.988 | 0.982 | 29 | 22 | 7 | 0.290 | -5.847 | 6.427 |
| F5 | R4 | 0.512 | 0.518 | 0.986 | 0.973 | 0.959 | 66 | 42 | 24 | -0.051 | -6.648 | 6.546 |
| F5 | R5 | 0.532 | 0.521 | 0.966 | 0.985 | 0.950 | 81 | 23 | 58 | -0.322 | -10.248 | 9.605 |
| F6 | R1 | 0.423 | 0.424 | 0.991 | 0.991 | 0.981 | 30 | 17 | 13 | 0.095 | -4.794 | 4.984 |
| F6 | R2 | 0.445 | 0.361 | 0.806 | 0.996 | 0.818 | 287 | 7 | 280 | -2.736 | -12.533 | 7.062 |
| F6 | R3 | 0.424 | 0.362 | 0.846 | 0.995 | 0.857 | 222 | 10 | 212 | -1.934 | -11.830 | 7.961 |
| F6 | R4 | 0.512 | 0.203 | 0.395 | 0.999 | 0.388 | 1009 | 2 | 1007 | -8.671 | -32.380 | 15.038 |
| F6 | R5 | 0.532 | 0.110 | 0.207 | 0.999 | 0.195 | 1372 | 2 | 1370 | -11.952 | -47.877 | 23.973 |

flips: patients whose category differs (up: exposed by pipeline only). R4/R5 at phase offset 0. mean_diff and limits of agreement in minutes below 65 mmHg.

## Table S3. POST HOC: probability that an episode is waveform-flagged, by elapsed time and nadir so far

| still < 65 mmHg after (s) | nadir_so_far | episodes | p_flagged |
|---|---|---|---|
| 10 | <20 | 1406 | 0.747 |
| 10 | 20-39 | 2046 | 0.792 |
| 10 | 40-54 | 3301 | 0.478 |
| 10 | 55-64 | 33017 | 0.016 |
| 30 | <20 | 384 | 0.594 |
| 30 | 20-39 | 704 | 0.574 |
| 30 | 40-54 | 2057 | 0.070 |
| 30 | 55-64 | 15900 | 0.009 |
| 60 | <20 | 224 | 0.442 |
| 60 | 20-39 | 300 | 0.080 |
| 60 | 40-54 | 2018 | 0.017 |
| 60 | 55-64 | 9413 | 0.007 |
| 120 | <20 | 159 | 0.289 |
| 120 | 20-39 | 248 | 0.024 |
| 120 | 40-54 | 1993 | 0.010 |
| 120 | 55-64 | 4911 | 0.006 |

Among episodes that had lasted at least the stated time; nadir so far = lowest monitor MAP up to that time.

## Table S4. POST HOC: depth-weighted exposures and lower thresholds (1-min median resolution)

| metric | thr | filter | res | or_ref | or_pipe | ror | lo | hi | p_perm |
|---|---|---|---|---|---|---|---|---|---|
| twa | 55 | F0 | R3 | 3.893 | 1.186 | 0.305 | 0.061 | 1.531 | 0.105 |
| twa | 55 | F1 | R3 | 3.893 | 4.065 | 1.044 | 0.401 | 2.715 | 0.880 |
| twa | 55 | F3 | R3 | 3.893 | 4.767 | 1.224 | 0.546 | 2.744 | 0.470 |
| twa | 65 | F0 | R3 | 1.266 | 1.169 | 0.923 | 0.788 | 1.083 | 0.235 |
| twa | 65 | F1 | R3 | 1.266 | 1.273 | 1.005 | 0.953 | 1.060 | 0.780 |
| twa | 65 | F3 | R3 | 1.266 | 1.269 | 1.002 | 0.958 | 1.048 | 0.870 |
| auc | 55 | F0 | R3 | 3.990 | 2.413 | 0.605 | 0.197 | 1.853 | 0.335 |
| auc | 55 | F1 | R3 | 3.990 | 3.339 | 0.837 | 0.406 | 1.726 | 0.565 |
| auc | 55 | F3 | R3 | 3.990 | 3.812 | 0.955 | 0.653 | 1.398 | 0.730 |
| auc | 65 | F0 | R3 | 1.242 | 1.217 | 0.980 | 0.911 | 1.054 | 0.605 |
| auc | 65 | F1 | R3 | 1.242 | 1.242 | 1.000 | 0.968 | 1.033 | 0.995 |
| auc | 65 | F3 | R3 | 1.242 | 1.247 | 1.004 | 0.981 | 1.028 | 0.705 |

| item | value |
|---|---|
| auc55_F0xR3_total_ratio | 1.5926511038398004 |
| auc55_F0xR3_excess_share | 0.3721160914722307 |
| auc55_F0xR3_top1pct_share_of_excess | 0.5633518466768042 |
| auc55_F1xR3_total_ratio | 1.1474727971391918 |
| auc55_F1xR3_excess_share | 0.12851964552611783 |
| auc55_F1xR3_top1pct_share_of_excess | 0.5537390027342186 |
| auc55_F3xR3_total_ratio | 0.9909324504685909 |
| auc55_F3xR3_excess_share | -0.009150522346019763 |
| auc55_F3xR3_top1pct_share_of_excess | -2.0514721232838955 |
| auc65_F0xR3_total_ratio | 1.1250310833187709 |
| auc65_F0xR3_excess_share | 0.11113567009183167 |
| auc65_F0xR3_top1pct_share_of_excess | 0.5190926964251571 |
| auc65_F1xR3_total_ratio | 1.0485801543205124 |
| auc65_F1xR3_excess_share | 0.04632946191127629 |
| auc65_F1xR3_top1pct_share_of_excess | 0.5245433707005375 |
| auc65_F3xR3_total_ratio | 1.0101195139055774 |
| auc65_F3xR3_excess_share | 0.01001813524664108 |
| auc65_F3xR3_top1pct_share_of_excess | 0.7610090577627407 |
| binary55_F0xR3 | ROR 1.19 (0.66–2.15) |
| binary55_F1xR3 | ROR 1.28 (0.81–2.02) |
| binary55_F3xR3 | ROR 1.10 (0.84–1.45) |
| binary60_F0xR3 | ROR 0.95 (0.79–1.14) |
| binary60_F1xR3 | ROR 0.98 (0.85–1.15) |
| binary60_F3xR3 | ROR 0.98 (0.84–1.13) |

TWA per mmHg; AUC (area under the threshold) per 100 mmHg·min, capped at the reference 99th centile. excess_share: fraction of the pipeline total area in excess of the reference total; top1pct_share: share of that excess contributed by the 1% of patients with the largest excess. Intervals as in A15.

## Table S5. Sensitivity analyses of the primary ROR (F1 × R3)

| analysis | ror | lo | hi | or_pipe | or_ref | events |
|---|---|---|---|---|---|---|
| reference=unbridged | 0.938 | 0.834 | 1.055 |  |  |  |
| reference=guard0 | 0.968 | 0.880 | 1.065 |  |  |  |
| reference=guard30 | 0.962 | 0.838 | 1.103 |  |  |  |
| reference=pp5 | 0.961 | 0.861 | 1.072 |  |  |  |
| reference=pp12 | 0.954 | 0.851 | 1.070 |  |  |  |
| reference=valid25 | 0.969 | 0.865 | 1.086 |  |  |  |
| reference=valid75 | 0.944 | 0.834 | 1.069 |  |  |  |
| reference=wavemean | 0.743 | 0.476 | 1.159 |  |  |  |
| S10 numerics-defined period | 0.910 | 0.747 | 1.107 |  |  |  |
| S5 + blood loss | 0.961 |  |  | 0.904 | 0.941 |  |
| S11 + number of postoperative creatinines | 0.949 |  |  | 0.845 | 0.890 |  |
| S7 AKI stage >= 2 (reduced set) | 0.968 |  |  | 2.143 | 2.215 | 24.000 |
| S4 missing postoperative creatinine = no AKI (pre-specified) | 0.963 | 0.865 | 1.071 |  |  | 91.000 |
| S6 transplantation included (pre-specified) | 0.958 | 0.866 | 1.060 |  |  | 122.000 |
| without gynaecology (low creatinine testing) | 0.959 | 0.857 | 1.073 |  |  | 89.000 |
| disease risk score, 2 df | 0.958 | 0.852 | 1.077 |  |  | 91.000 |
| reference=concord | 0.963 | 0.854 | 1.087 |  |  | 91.000 |
| reference=valid25_obs | 0.949 | 0.850 | 1.060 |  |  | 91.000 |
| reference=valid75_obs | 0.952 | 0.832 | 1.090 |  |  | 91.000 |

Rows from the frozen run first; S4, S6 (pre-specified, run after unblinding) and post hoc rows after. Rows without lo/hi are point estimates.

## Table S6. Differential misclassification: AKI on spurious minutes per hour, adjusted for reference exposure

| pipeline | model | term | nonzero | or_per_sd | lo | hi | or_per_log1p | lo_u | hi_u |
|---|---|---|---|---|---|---|---|---|---|
| F1xR3 | b_g1_zero_high | 0 | 19.000 | 1.022 | 0.829 | 1.259 | 1.892 | 0.004 | 966.903 |
| F1xR3 | b_g2_nonpuls_noise | 0 | 168.000 | 0.895 | 0.695 | 1.153 | 0.266 | 0.013 | 5.480 |
| F1xR3 | b_all | 0 | 241.000 | 0.831 | 0.626 | 1.102 | 0.159 | 0.010 | 2.614 |
| F1xR3 | c_negative_control | 0 | 241.000 | 0.832 | 0.628 | 1.103 | 0.161 | 0.010 | 2.641 |
| F1xR3 | c_negative_control | 1 | 688.000 | 1.135 | 0.936 | 1.376 | 2.039 | 0.690 | 6.027 |
| F1xR3 | d_mechanism | 0 | 241.000 | 0.837 | 0.632 | 1.107 | 0.170 | 0.011 | 2.740 |
| F1xR3 | d_mechanism | 1 | 2.49e+03 | 0.978 | 0.772 | 1.239 | 0.940 | 0.492 | 1.797 |
| F1xR3 | d_mechanism | 2 | 2.56e+03 | 1.188 | 0.938 | 1.504 | 1.197 | 0.936 | 1.530 |
| F1xR3 | d_mechanism | 3 | 190.000 | 1.025 | 0.927 | 1.134 | 1.001 | 0.996 | 1.007 |
| F0xR1 | b_g1_zero_high | 0 | 789.000 | 1.105 | 0.938 | 1.300 | 17.314 | 0.162 | 1.85e+03 |
| F0xR1 | b_g2_nonpuls_noise | 0 | 1.4e+03 | 0.878 | 0.695 | 1.110 | 0.288 | 0.031 | 2.710 |
| F0xR1 | b_all | 0 | 1.73e+03 | 0.928 | 0.741 | 1.161 | 0.589 | 0.122 | 2.855 |
| F0xR1 | c_negative_control | 0 | 1.73e+03 | 0.916 | 0.731 | 1.148 | 0.539 | 0.110 | 2.636 |
| F0xR1 | c_negative_control | 1 | 1.94e+03 | 1.171 | 0.957 | 1.433 | 2.095 | 0.815 | 5.383 |
| F0xR1 | d_mechanism | 0 | 1.73e+03 | 0.922 | 0.737 | 1.153 | 0.563 | 0.116 | 2.722 |
| F0xR1 | d_mechanism | 1 | 2.49e+03 | 0.971 | 0.766 | 1.231 | 0.923 | 0.482 | 1.768 |
| F0xR1 | d_mechanism | 2 | 2.56e+03 | 1.199 | 0.947 | 1.517 | 1.208 | 0.945 | 1.544 |
| F0xR1 | d_mechanism | 3 | 190.000 | 1.026 | 0.928 | 1.135 | 1.001 | 0.996 | 1.007 |
| F0xR1 (separate model) | spurious_hypo | 0 |  | 0.928 | 0.741 | 1.161 | 0.589 | 0.122 | 2.855 |
| F0xR1 (separate model) | spurious_hyper_negative_control | 0 |  | 1.164 | 0.952 | 1.424 | 2.038 | 0.793 | 5.236 |

term 0: log(1 + spurious min/h) (or group-specific version); c_negative_control term 1: spurious hypertensive min/h; d_mechanism terms 1–3: blood gases/h, log blood loss, red-cell units. lo/hi per SD; lo_u/hi_u per unit of log(1 + min/h).

## Table S7. Discordant patients, operating characteristics of the equivalence decision, and interval coverage

| pipeline | up | aki_up | down | aki_down |
|---|---|---|---|---|
| F1xR3 | 28 | 0 | 5 | 0 |
| F0xR1 | 55 | 4 | 1 | 0 |
| F3xR2 | 50 | 3 | 4 | 0 |
| F6xR3 | 8 | 0 | 178 | 3 |

F1 × R3: expected AKI among the 33 discordant patients 1.57; probability of none 0.19.

| k | ror | lo | hi | n | events | verdict |
|---|---|---|---|---|---|---|
| 0 | 0.956 | 0.856 | 1.068 | 2563 | 91 | equivalent |
| 1 | 1.013 | 0.901 | 1.138 | 2563 | 91 | equivalent |
| 2 | 1.070 | 0.900 | 1.272 | 2563 | 91 | inconclusive |
| 3 | 1.129 | 0.938 | 1.358 | 2563 | 91 | inconclusive |
| 4 | 1.195 | 0.957 | 1.492 | 2563 | 91 | inconclusive |
| 5 | 1.269 | 0.982 | 1.641 | 2563 | 91 | inconclusive |

ROR and A15 interval if k of the 28 upward-moved patients had developed AKI (outcomes swapped with k concordant cases; 400 bootstrap resamples, 200 permutations). Under the reference model, P(k = 0) = 0.26, P(k = 1) = 0.38, P(k ≥ 2) = 0.36.

| scenario | gamma_up | median_ror | p_equivalent | coverage_of_1 | sd_lror | n |
|---|---|---|---|---|---|---|
| null | 0.000 | 1.004 | 0.820 | 0.970 | 0.062 | 200 |
| upper_margin | 1.912 | 1.239 | 0.050 | 0.510 | 0.098 | 200 |

Simulated outcomes from the fully adjusted reference model; differential error added as a log-odds shift γ in upward-moved patients. Each dataset analysed with the A15 rule (200 bootstrap resamples, 200 permutations). Median ROR by γ: up0.0: 0.99, up1.0: 1.08, up2.0: 1.27, up3.0: 1.52, up4.0: 1.89, down2.0: 0.95, down4.0: 0.86, down8.0: 0.78. Coverage of 1 under independent permutations (SD from the dry run, 100 calibration datasets): F1xR3 1.00, F0xR1 0.99, F3xR2 1.00, F6xR3 0.97.

## Table S8. Injection–recovery sweep (post hoc)

| kind | param | any_artefact | frac_artefact |
|---|---|---|---|
| flush | (120, 0.5) | 0.000 | 0.000 |
| flush | (120, 1) | 0.000 | 0.000 |
| flush | (120, 2) | 1.000 | 0.100 |
| flush | (120, 4) | 1.000 | 0.200 |
| flush | (150, 0.5) | 0.000 | 0.000 |
| flush | (150, 1) | 0.000 | 0.000 |
| flush | (150, 2) | 1.000 | 0.100 |
| flush | (150, 4) | 1.000 | 0.200 |
| flush | (200, 0.5) | 0.000 | 0.000 |
| flush | (200, 1) | 0.000 | 0.000 |
| flush | (200, 2) | 1.000 | 0.100 |
| flush | (200, 4) | 1.000 | 0.200 |
| flush | (250, 0.5) | 1.000 | 0.100 |
| flush | (250, 1) | 1.000 | 0.100 |
| flush | (250, 2) | 1.000 | 0.100 |
| flush | (250, 4) | 1.000 | 0.200 |
| flush | (300, 0.5) | 1.000 | 0.100 |
| flush | (300, 1) | 1.000 | 0.100 |
| flush | (300, 2) | 1.000 | 0.100 |
| flush | (300, 4) | 1.000 | 0.200 |
| zero_level | 0 | 1.000 | 0.500 |
| zero_level | 5 | 1.000 | 0.500 |
| zero_level | 10 | 1.000 | 0.500 |
| zero_level | 15 | 1.000 | 0.500 |
| zero_level | 20 | 1.000 | 0.500 |
| zero_level | 25 | 1.000 | 0.500 |
| damping_hz | 1.5 | 0.118 | 0.079 |
| damping_hz | 2 | 0.008 | 0.001 |
| damping_hz | 3 | 0.000 | 0.000 |
| damping_hz | 5 | 0.000 | 0.000 |
| damping_hz | 10 | 0.000 | 0.000 |
| partial_occlusion | 0.5 | 0.000 | 0.000 |
| partial_occlusion | 0.3 | 0.025 | 0.010 |
| partial_occlusion | 0.15 | 0.613 | 0.520 |
| drift_mmhg | 10 | 0.008 | 0.001 |
| drift_mmhg | 20 | 0.008 | 0.001 |
| drift_mmhg | 40 | 0.008 | 0.006 |
| ringing_mmhg | 5 | 0.000 | 0.000 |
| ringing_mmhg | 10 | 0.000 | 0.000 |
| ringing_mmhg | 20 | 0.008 | 0.001 |
| sampling_no_flush | mean | 1.000 | 0.700 |
| sampling_no_flush | 20 | 1.000 | 0.700 |

any_artefact: share of injections with at least one window in the injected 20 s labelled artefact (zero/high/non-pulsatile/noise; guard excluded); 119 clean 2-min segments from 60 cases.

## Table S9. Blinded AI rating of 152 snippets (secondary)

| item | value |
|---|---|
| n_rated | 152.000 |
| n | 131.000 |
| agree | 0.977 |
| kappa | 0.954 |
| artefact_share_in_subset | 0.435 |
| alg_artefact_rated_artefact | 1.000 |
| alg_valid_rated_artefact | 0.041 |
| alg_valid_n | 74.000 |
| alg_valid_low_strata_n | 36.000 |
| guard_n | 19.000 |
| guard_rated_artefact | 0.684 |
| unsure | 2.000 |

## Table S10. In-hospital mortality (exploratory, reduced adjustment set)

n = 2962, deaths = 26; OR reference 1.50 (0.69–3.27); OR F1 × R3 1.47 (0.68–3.20); ROR 0.98.

## Table S11. Odds ratios for AKI by adjustment level (AKI set, 1-min median)

| series | exposure | adjustment | odds_ratio | lo | hi |
|---|---|---|---|---|---|
| reference | binary65 | crude | 1.655 | 1.090 | 2.513 |
| reference | binary65 | reduced_set | 1.463 | 0.952 | 2.248 |
| reference | binary65 | full_set | 0.940 | 0.596 | 1.483 |
| reference | binary65 | full_set_without_duration | 1.097 | 0.704 | 1.709 |
| reference | binary55 | crude | 3.813 | 1.865 | 7.794 |
| reference | binary55 | reduced_set | 3.362 | 1.575 | 7.180 |
| reference | binary55 | full_set | 1.954 | 0.894 | 4.270 |
| reference | minutes65 | crude | 1.215 | 1.136 | 1.300 |
| reference | minutes65 | reduced_set | 1.195 | 1.112 | 1.283 |
| reference | minutes65 | full_set | 1.079 | 0.994 | 1.172 |
| F1xR3 | binary65 | crude | 1.593 | 1.049 | 2.419 |
| F1xR3 | binary65 | reduced_set | 1.414 | 0.921 | 2.170 |
| F1xR3 | binary65 | full_set | 0.899 | 0.571 | 1.417 |
| F1xR3 | binary55 | crude | 4.673 | 2.465 | 8.857 |
| F1xR3 | binary55 | reduced_set | 4.106 | 2.068 | 8.151 |
| F1xR3 | binary55 | full_set | 2.494 | 1.224 | 5.080 |
| F1xR3 | minutes65 | crude | 1.221 | 1.142 | 1.305 |
| F1xR3 | minutes65 | reduced_set | 1.200 | 1.119 | 1.288 |
| F1xR3 | minutes65 | full_set | 1.087 | 1.002 | 1.179 |

reduced_set: age and eGFR splines, ASA ≥ 3, emergency. Wald intervals from Firth fits. AKI-set inclusion by department: General surgery 85% of 1749, Gynecology 28% of 172, Thoracic surgery 96% of 996, Urology 97% of 59.
