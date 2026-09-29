from pathlib import Path
import numpy as np
import pandas as pd


def load_csv_directory(data_dir: str | Path) -> pd.DataFrame:
    data_dir = Path(data_dir)
    files = sorted(data_dir.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {data_dir}")
    frames = [pd.read_csv(path, low_memory=False) for path in files]
    return pd.concat(frames, ignore_index=True)


def prepare_binary_data(df: pd.DataFrame):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    label_candidates = [c for c in df.columns if c.lower() == "label"]
    if not label_candidates:
        raise ValueError("Expected a 'Label' column in the dataset.")
    label_col = label_candidates[0]

    y = (~df[label_col].astype(str).str.strip().str.upper().eq("BENIGN")).astype(int)
    X = df.drop(columns=[label_col])
    X = X.select_dtypes(include=[np.number]).replace([np.inf, -np.inf], np.nan)
    X = X.dropna(axis=1, how="all")
    return X, y
