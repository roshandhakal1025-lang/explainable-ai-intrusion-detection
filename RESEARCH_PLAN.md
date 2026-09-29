# Research plan

## Objective
Evaluate the trade-off between predictive performance and interpretability in machine-learning network intrusion detection.

## Primary question
How accurately can supervised ML models distinguish benign from malicious network traffic, and which features most strongly influence their decisions?

## Experimental design
- Dataset: CICIDS2017
- Task: binary intrusion classification
- Baseline: Logistic Regression
- Main model: Random Forest
- Split: stratified 80/20 holdout with fixed seed
- Metrics: precision, recall, F1, ROC-AUC, confusion matrix, false-positive behavior
- Explainability: SHAP global and local explanations

## Threats to validity
Benchmark traffic may not represent contemporary production networks. Random splitting may permit temporal or scenario leakage. Dataset imbalance can distort aggregate metrics. Feature importance is model-dependent and is not causal evidence.

## Next experiments
1. Establish reproducible baseline results.
2. Compare random and time-aware splits where feasible.
3. Add precision-recall AUC.
4. Analyze false positives by traffic characteristics.
5. Compare explanation stability across seeds/models.
6. Test cross-dataset generalization.
