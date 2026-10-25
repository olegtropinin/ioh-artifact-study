# Novelty check, round 1 (2026-10-26, literature agent, ~55 searches)

## Closest prior work
- Pasma W, Peelen LM, van Buuren S, van Klei WA, de Graaff JC. Artifact processing methods influence on intraoperative hypotension quantification and outcome effect estimates. Anesthesiology 2020;132:723-737. doi:10.1097/ALN.0000000000003131. 8 published filters, 2,988 cases, per-minute AIMS data; hypotension MAP<50 incidence 24% (7-point median filter) to 55% (no filter); association with myocardial injury changed little.
- Jacobsson M, Valadkhani A, Winski G, Bell M. Accuracy of quantifying hypotension during surgery using physiological sensor data. IEEE J Transl Eng Health Med 2026;14:265-273. doi:10.1109/JTEHM.2026.3698197. 125 Hz reference, 419 patients (+VitalDB supplement); coarser sampling inflates minutes-below-threshold (+30% at 15 s); outcome effect only extrapolated. Single artifact rule: ABP outside 15-250, beat MAP outside 35-150, PP<15.
- Pasma W et al. Artifacts annotations in anesthesia blood pressure data by man and machine. J Clin Monit Comput 2021. doi:10.1007/s10877-020-00574-z. Live-observed artifacts (flush, sampling, NIBP same arm, transducer height); retrospective review finds only 32%.
- Kool NP et al. Can J Anaesth 2012;59:833-841 (PMID 22806063): invasive BP artifacts 14% of per-minute AIMS values.
- Du CH, Glick D, Tung A. J Clin Monit Comput 2019;33:407-412: neighbour-comparison algorithm, sensitivity 87%.
- Khan JM, Maslove DM, Boyd JG. Crit Care Explor 2022;4:e0814. doi:10.1097/cce.0000000000000814: MAP limits 30-200.
- Maleczek M et al. Anesthesiology 2024;141:32-43. doi:10.1097/aln.0000000000004971: artifact detectors have low sensitivity.
- Bergmann T et al. Physiol Rep 2025;13:e70533. doi:10.14814/phy2.70533: scoping review; effect of artifact handling on outcomes "not thoroughly examined".
- Vernooij LM et al. Br J Anaesth 2018;120:1080-1089. doi:10.1016/j.bja.2018.01.033: IOH modelling choices change ORs.
- Wesselink EM et al. Br J Anaesth 2018;121:706-721. doi:10.1016/j.bja.2018.04.036: definition heterogeneity.
- Maleczek M et al. PLoS One 2024;19:e0312966. doi:10.1371/journal.pone.0312966: many IOH definitions, one cleaning rule.
- Packiasabapathy S et al. F1000Research 2018;7:275. doi:10.12688/f1000research.13810.1: beat vs 15-s resolution.
- Kouz K et al. Anesthesiology 2026;145:291-299. doi:10.1097/aln.0000000000006140: 2.5 vs 5-min oscillometry.
- Sessler DI et al. POQI consensus. Br J Anaesth 2019;122:563-574. doi:10.1016/j.bja.2019.01.013.

## VitalDB IOH-AKI papers (each uses one cleaning rule, no sensitivity analysis)
- Lee SB. J Pers Med 2026;16:371. doi:10.3390/jpm16070371 - waveform 100 Hz, n=2,726, exclude values outside 20-250.
- Ensarioglu M, Yildirim AK. J Clin Med 2026;15:6871. doi:10.3390/jcm15176871 - TWA-MAP<65, rule not stated in abstract.
- Folks R ... Naik BI. BMC Anesthesiol 2024;24:395. doi:10.1186/s12871-024-02784-3 - "artifact reduction algorithm", rules not given.

## Methods references
- Zong W et al. Comput Cardiol 2003;30:259-262 (wabp). Sun JX, Reisner AT, Mark RG. Comput Cardiol 2006;33:13-16 (ABP SQI).
- Li Q, Mark RG, Clifford GD. Biomed Eng Online 2009;8:13. doi:10.1186/1475-925X-8-13 - artifact models for injection.
- Simonsohn U, Simmons JP, Nelson LD. Specification curve analysis. Nat Hum Behav 2020;4:1208-1214.
- Steegen S et al. Increasing transparency through a multiverse analysis. Perspect Psychol Sci 2016;11:702-712.

## Not found (queries in agent report)
No multiverse/specification-curve analysis in anaesthesiology; no study estimating AKI association across resolution x artifact rule on one cohort; no VitalDB artifact label set.
