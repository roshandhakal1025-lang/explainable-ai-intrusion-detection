# Final Research Report

## Title
**Explainable Machine Learning for Network Intrusion Detection: Evaluating the Generalization Gap in CICIDS2017**

## Abstract
This project evaluates binary network-intrusion detection using Logistic Regression and tree ensembles on CICIDS2017, with emphasis on whether strong benchmark performance survives distribution shift. A deterministic 124,182-flow development sample was constructed from all eight MachineLearningCSV files while preserving source-file provenance. Under a conventional random stratified split, Random Forest achieved attack F1 of 0.9971 and recall of 0.9971. Under a Friday cross-scenario holdout, its attack F1 fell to approximately 0.44 and recall to approximately 0.285. Family-level analysis localized the failure: DDoS remained partly detectable, whereas Bot and PortScan were almost completely missed. SHAP identified Destination Port, packet-length statistics, and TCP initial-window features as major model drivers. Validation-based threshold tuning improved Friday recall to 0.4652 but raised the false-positive rate to 5.83%; class-weight changes produced little improvement. The results show that random flow-level evaluation can be substantially more optimistic than a cross-scenario stress test on this benchmark and that aggregate discrimination metrics can obscure operational failure modes.

## Research question
How accurately can supervised machine-learning models distinguish benign from malicious network traffic, which network features most strongly influence their predictions, and how robust are those predictions under cross-scenario distribution shift?

## Method
CICIDS2017 contains labeled flow records collected across multiple days and attack scenarios. The supplied MachineLearningCSV archive contains 2,830,743 flows. Because full in-memory fitting exceeded the available execution environment, the reported development experiment uses a deterministic seed-42 sample capped at 10,000 benign and 10,000 attack observations per source file. Numeric features are converted to float32; infinite values become missing values; all-missing columns are removed; median imputation is applied inside each model pipeline.

Two primary evaluation designs are used: (1) an 80/20 stratified random split and (2) a Friday holdout trained on sampled Monday-Thursday traffic. The second design deliberately stresses generalization but is not a pure temporal experiment because attack-family composition also changes.

## Results
Random Forest appears nearly perfect under the random split (ROC-AUC 0.9999, PR-AUC 0.9998, attack F1 0.9971). The same model performs much worse on the Friday stress test, with attack recall around 0.285 and F1 around 0.44. Logistic Regression also degrades but has higher Friday F1 than Random Forest in the primary run.

Friday family analysis shows that Random Forest detects roughly 62% of DDoS in the repeated failure-analysis run, but essentially 0% of Bot and about 0.2% of PortScan. This demonstrates that the aggregate recall loss is concentrated in specific novel scenarios rather than being uniform.

SHAP analysis ranks Destination Port highest in mean absolute contribution, followed by packet-length and TCP-window features. These values describe the fitted model's decision behavior and do not establish causality.

A validation-selected threshold of 0.09 raises Friday attack recall from 0.2843 to 0.4652 and F1 from 0.4418 to 0.6023, but false-positive rate rises from 0.21% to 5.83%. Reweighting attack observations by 2x or 4x does not materially improve recall. Extra Trees likewise fails to solve the family-shift problem.

## Discussion
The experiment demonstrates why intrusion-detection evaluation should include distribution-shift tests. Random splitting allows flows generated under similar scenarios to appear in both train and test partitions, producing a much easier interpolation problem. Holding out Friday changes the task to one that includes attack families/scenarios not represented identically in training. The resulting performance collapse is therefore consistent with scenario-specific learning.

The threshold experiment adds an operational perspective. A lower threshold can recover DDoS sensitivity, but it produces many more benign alerts and still does not meaningfully detect Bot or PortScan. This means the problem cannot be reduced to choosing a more aggressive threshold. The class-weight experiment reaches the same conclusion from another direction.

## Limitations
This is a development-scale sample rather than full-dataset model fitting. Friday holdout confounds day, scenario, and attack family, so it cannot isolate temporal drift. CICIDS2017 reflects a controlled 2017 environment and should not be treated as current production traffic. Extremely rare classes limit attack-specific inference. SHAP explanations are model-dependent. Repeated seeds and an external dataset would be required before making broader generalization claims.

## Conclusion
The project finds a large and practically important gap between random-split benchmark performance and cross-scenario attack detection. The most defensible conclusion is methodological: **near-perfect random-split scores are insufficient evidence of robust intrusion detection on this experiment.** Evaluation should report attack recall, false-positive behavior, family-level failures, and performance under meaningful distribution shift.

## Next research extensions
The strongest extensions for a formal thesis would be repeated-seed confidence intervals, leave-one-day/leave-one-attack-family-out evaluation, external validation on a second IDS dataset, probability calibration, and drift-aware or anomaly-detection approaches. Those are intentionally identified as future research rather than presented as completed evidence.
