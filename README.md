# Explainable AI for Network Intrusion Detection

A reproducible research project investigating whether machine-learning intrusion detection systems can combine strong predictive performance with explanations that are useful for understanding network-security decisions.

## Research question

**How accurately can supervised machine-learning models distinguish benign from malicious network traffic, and which network features most strongly influence their predictions?**

### Hypotheses
- H1: Tree-based models will outperform a simple logistic-regression baseline on intrusion-detection metrics.
- H2: Explainability methods such as SHAP will identify a relatively small subset of network-flow features that strongly influence predictions.
- H3: False-positive analysis will reveal recurring patterns that are not obvious from aggregate accuracy alone.

## Why this matters

Intrusion detection is a high-dimensional classification problem where accuracy alone is insufficient. Security analysts also need to understand why a model flags traffic. This project therefore evaluates both **predictive performance** and **model interpretability**.

## Planned dataset

The initial experiment is designed for the **CICIDS2017** network intrusion dataset from the Canadian Institute for Cybersecurity. Raw data is intentionally not committed to this repository. See `data/README.md` for setup guidance.

## Methodology

1. Load and validate network-flow data.
2. Clean missing/infinite values and normalize labels.
3. Create a binary benign-vs-attack target.
4. Use a stratified train/test split.
5. Establish a Logistic Regression baseline.
6. Train a Random Forest classifier.
7. Compare precision, recall, F1, ROC-AUC, confusion matrices, and false-positive rates.
8. Use SHAP to investigate global and local feature importance.
9. Analyze misclassified traffic and document limitations.\n\n## Current headline result\n\nRandom-split performance substantially overstates cross-day generalization in the current experiment. Random Forest attack recall fell from **0.9971** on the random split to **0.2854** on the Friday holdout. See `RESULTS.md`.

## Repository structure

```
.
├── data/                  # dataset instructions; raw data excluded
├── notebooks/             # exploratory/research notebooks
├── src/
│   ├── data.py            # preprocessing
│   ├── train.py           # model training/evaluation
│   └── explain.py         # SHAP explainability
├── tests/                 # lightweight preprocessing tests
├── .gitignore
├── requirements.txt
└── README.md
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Place CICIDS2017 CSV files under data/raw/
python -m src.train --data-dir data/raw
```

## Evaluation principles

Accuracy can be misleading for imbalanced cybersecurity data. The analysis therefore emphasizes precision, recall, F1, ROC-AUC, confusion matrices, and false positives. A future extension will add precision-recall AUC and attack-family multiclass evaluation.

## Research status

**Phase 2 — first real experiments completed.** On a deterministic 124,182-flow development sample, Random Forest achieved attack F1=0.9971 under a random split but only F1=0.4431 on a Friday cross-day holdout. This large generalization gap is the central finding so far. See `RESULTS.md` for the full metrics, interpretation, and limitations.

## Future extensions

- Multiclass attack-family classification
- XGBoost/LightGBM comparison
- Class-imbalance experiments
- SHAP stability analysis
- Cross-dataset generalization
- Adversarial robustness
- Reproducible experiment tracking

## Ethics and limitations

This project is intended for defensive cybersecurity research. Dataset labels, collection conditions, class imbalance, temporal leakage, and differences between benchmark traffic and modern production networks can limit generalizability. Explainability scores describe model behavior; they do not establish causal relationships.

## Author

Roshan Dhakal

Research portfolio project for graduate study in artificial intelligence and cybersecurity.
