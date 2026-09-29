# Dataset profile — CICIDS2017 MachineLearningCSV

The uploaded official archive was inspected before modeling.

| Source CSV | Rows | Attack labels |
|---|---:|---|
| Monday | 529,918 | Benign only |
| Tuesday | 445,909 | FTP-Patator, SSH-Patator |
| Wednesday | 692,703 | DoS Hulk, GoldenEye, slowloris, Slowhttptest, Heartbleed |
| Thursday morning | 170,366 | Web Attack Brute Force, XSS, SQL Injection |
| Thursday afternoon | 288,602 | Infiltration |
| Friday morning | 191,033 | Bot |
| Friday afternoon PortScan | 286,467 | PortScan |
| Friday afternoon DDoS | 225,745 | DDoS |

**Total: 2,830,743 flows.**

The rarest classes are extremely small (e.g. Heartbleed 11 and Infiltration 36 observations), which is an important limitation for multiclass conclusions.

## Engineering decision

Loading and fitting the complete benchmark in one in-memory pandas/scikit-learn process exceeded the available research execution environment. The development experiment therefore uses a documented, deterministic per-file sample (seed 42), capped separately for benign and attack observations. This preserves all source days and rare attacks while keeping the experiment reproducible.

The repository retains a day-aware Friday holdout to expose distribution shift that a random row split can hide. Full-scale/out-of-core training is a later experiment, not silently substituted with invented results.
