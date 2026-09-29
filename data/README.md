# Dataset setup

This project is designed initially around CICIDS2017 network-flow CSV data.

1. Obtain the dataset from the official Canadian Institute for Cybersecurity source.
2. Place extracted CSV files in `data/raw/`.
3. Do not commit raw dataset files to GitHub.
4. Run `python -m src.train --data-dir data/raw`.

The loader combines CSV files, normalizes column names, cleans infinite values, and converts labels into a binary target: benign = 0, attack = 1.
