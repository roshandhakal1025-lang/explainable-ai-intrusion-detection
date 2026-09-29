# CICIDS2017 dataset setup

Use the official CICIDS2017 MachineLearningCSV distribution from the Canadian Institute for Cybersecurity (CIC), University of New Brunswick.

Official dataset page: https://www.unb.ca/cic/datasets/ids-2017.html

## Setup

1. Download the machine-learning CSV distribution from the official page.
2. Extract it under `data/raw/`.
3. Preserve the original CSV filenames because the day-aware experiment uses filename provenance.

The raw benchmark is deliberately excluded from Git.

## Experiments

Random stratified baseline:

```bash
python -m src.train --data-dir data/raw --split-strategy random
```

Cross-day holdout using Friday as test data:

```bash
python -m src.train --data-dir data/raw --split-strategy day-aware
```

Outputs go to `artifacts/random/` and `artifacts/day-aware/`.

## Citation

Sharafaldin, I., Habibi Lashkari, A., & Ghorbani, A. A. (2018). *Toward generating a new intrusion detection dataset and intrusion traffic characterization*. ICISSP.
