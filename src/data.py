from pathlib import Path
import numpy as np
import pandas as pd


def load_csv_directory(data_dir: str | Path) -> pd.DataFrame:
    data_dir = Path(data_dir)
    files = sorted(data_dir.rglob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found under {data_dir}")
    frames = []
    for path in files:
        frame = pd.read_csv(path, low_memory=False)
        frame["__source_file"] = path.name
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def prepare_binary_data(df: pd.DataFrame):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    labels = [c for c in df.columns if c.lower() == "label"]
    if not labels:
        raise ValueError("Expected a 'Label' column in the dataset.")
    label_col = labels[0]
    y = (~df[label_col].astype(str).str.strip().str.upper().eq("BENIGN")).astype(int)
    source = df["__source_file"].copy() if "__source_file" in df else pd.Series("unknown", index=df.index)
    X = df.drop(columns=[label_col, "__source_file"], errors="ignore")
    X = X.select_dtypes(include=[np.number]).replace([np.inf, -np.inf], np.nan)
    X = X.dropna(axis=1, how="all")
    X = X.loc[:, ~X.columns.duplicated()]
    return X, y, source
