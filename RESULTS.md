# Experimental results

## Scope

These are real results produced from the official CICIDS2017 MachineLearningCSV archive supplied for this project. To fit the available execution environment, the development experiment used a deterministic per-file sample (seed 42): up to 10,000 benign and 10,000 attack flows from each CSV. The resulting sample contained **124,182 flows and 78 numeric features**.

This is a development-scale experiment, not a claim of full-dataset performance.

## 1. Random stratified split

| Model | ROC-AUC | PR-AUC | Attack precision | Attack recall | Attack F1 | False-positive rate |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.9697 | 0.9408 | 0.8643 | 0.9496 | 0.9049 | 0.0824 |
| Random Forest | 0.9999 | 0.9998 | 0.9972 | 0.9971 | 0.9971 | 0.0016 |

Random Forest confusion matrix: TN=15,975, FP=25, FN=26, TP=8,811.

## 2. Day-aware Friday holdout

Training used sampled Monday-Thursday flows; testing used sampled Friday flows. This deliberately evaluates distribution shift and includes Friday attack families not represented identically in earlier days.

| Model | ROC-AUC | PR-AUC | Attack precision | Attack recall | Attack F1 | False-positive rate |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8220 | 0.8068 | 0.8776 | 0.3825 | 0.5327 | 0.0391 |
| Random Forest | 0.7489 | 0.7194 | 0.9901 | 0.2854 | 0.4431 | 0.0021 |

Random Forest confusion matrix: TN=29,937, FP=63, FN=15,696, TP=6,270.

## Main finding

The random split gives extremely strong Random Forest performance, but that result does **not** generalize to the cross-day holdout. Attack recall falls from **0.9971 to 0.2854** for Random Forest. Logistic Regression also degrades substantially, although its Friday recall (0.3825) is higher than Random Forest.

This gap is the most important result so far. It shows why a random row split can substantially overstate practical intrusion-detection performance when train and test data share scenario-specific structure. The day-aware test is not a perfect deployment simulation, but it is a materially harder generalization test.

## Explainability

SHAP was computed on 500 reproducibly sampled flows for the random-split Random Forest. Highest mean absolute SHAP features were:

| Rank | Feature | Mean abs. SHAP |
|---:|---|---:|
| 1 | Destination Port | 0.0582 |
| 2 | Min Packet Length | 0.0314 |
| 3 | Init_Win_bytes_backward | 0.0293 |
| 4 | Init_Win_bytes_forward | 0.0261 |
| 5 | Fwd Packet Length Mean | 0.0229 |
| 6 | Fwd Packet Length Min | 0.0187 |
| 7 | Bwd Packet Length Std | 0.0181 |
| 8 | Packet Length Variance | 0.0180 |

These are explanations of model behavior, not evidence that the features causally produce attacks.

## Interpretation

H1 is supported only under the random split; it is **not supported under the Friday holdout**, where Logistic Regression has higher ROC-AUC, PR-AUC, recall, and F1 than Random Forest. H2 receives preliminary support because SHAP importance is concentrated among a subset of flow/packet features, but stability across seeds and splits still needs testing. H3 remains an active analysis target.

## Limitations

- Development-scale deterministic sample rather than full-dataset fitting.
- Friday holdout changes both time/scenario and attack-family composition, so degradation cannot be attributed to time alone.
- CICIDS2017 is a benchmark collected in 2017 and does not represent all contemporary network environments.
- Rare classes such as Heartbleed and Infiltration are too small for strong class-specific conclusions.
- Random Forest/SHAP importance is model-dependent and non-causal.


## Friday attack-family failure analysis

A second reproducible run (same seed and 10,000-per-class/file development cap) examined Friday predictions by attack family. Small metric differences from the first run reflect the explicitly documented development sampling configuration.

### Random Forest

| Friday class | Test flows | Predicted as attack | Detection rate |
|---|---:|---:|---:|
| Bot | 1,966 | 0 | **0.00%** |
| DDoS | 10,000 | 6,263 | **62.63%** |
| PortScan | 10,000 | 26 | **0.26%** |
| Benign | 30,000 | 53 false alarms | 99.82% benign specificity |

Overall Friday attack recall was **28.63%** with **99.16% attack precision**.

This localizes the generalization failure: the model is not uniformly weak on Friday. It detects a substantial fraction of DDoS, but almost completely misses Bot and PortScan traffic.

### Alternative tree ensemble

Extra Trees was tested as a simple model-family mitigation rather than assuming Random Forest was uniquely responsible for the failure.

| Model | Friday ROC-AUC | Friday PR-AUC | Attack recall | Attack F1 |
|---|---:|---:|---:|---:|
| Random Forest | 0.7726 | 0.7377 | **0.2863** | **0.4443** |
| Extra Trees | **0.8592** | **0.7849** | 0.0984 | 0.1742 |

Extra Trees improves ranking metrics but performs worse at the default classification threshold. It detects 21.5% of DDoS, 0% of Bot, and 0.11% of PortScan. Therefore simply swapping tree ensembles does **not** solve cross-day attack detection.

### What this tells us

The failure is strongly associated with attack-family/distribution shift. Friday introduces Bot, PortScan, and DDoS scenarios while the training days contain different attack families. Consequently, the Friday experiment is best interpreted as a **cross-scenario / novel-family generalization stress test**, not merely a temporal holdout.

The result also shows why ROC-AUC alone is insufficient: Extra Trees has a higher Friday ROC-AUC than Random Forest while its default-threshold attack recall is much worse. Operational threshold behavior must therefore be reported alongside ranking metrics.
