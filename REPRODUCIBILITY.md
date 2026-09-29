# Reproducibility

- Python dependencies are pinned by minimum compatible versions in `requirements.txt`.
- All reported development sampling uses random seed **42**.
- Reported cap: **10,000 benign + 10,000 attack flows per source CSV**.
- Raw CICIDS2017 data is not committed.
- `src/train.py` reproduces random and Friday holdout model runs.
- `src/explain.py` reproduces SHAP feature importance after model training.
- `src/failure_analysis.py` summarizes predictions by original attack label.
- `src/threshold_analysis.py` selects a threshold using validation data rather than the Friday test set.
- Machine-readable outputs are under `results/`; presentation figures are under `figures/`.

## Important experimental boundary

The Friday test set must remain untouched when selecting hyperparameters or thresholds. Threshold selection is performed on a validation subset of Monday-Thursday data. Friday is used only for final stress-test evaluation.

The full 2.83-million-flow benchmark was profiled, but the reported model results are explicitly development-sample results because full in-memory fitting exceeded the execution environment.
