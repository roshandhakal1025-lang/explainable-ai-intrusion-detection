from pathlib import Path
import numpy as np
import pandas as pd


def iter_csv_files(data_dir):
    files = sorted(Path(data_dir).rglob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found under {data_dir}")
    return files


def load_research_sample(data_dir, benign_per_file=25000, attack_per_file=25000, seed=42):
    """Memory-safe, reproducible sample preserving every source day/file."""
    frames = []
    for path in iter_csv_files(data_dir):
        df = pd.read_csv(path, low_memory=False)
        df.columns = [str(c).strip() for c in df.columns]
        label_col = next((c for c in df.columns if c.lower() == "label"), None)
        if label_col is None:
            raise ValueError(f"No Label column in {path.name}")
        labels = df[label_col].astype(str).str.strip()
        benign = df[labels.str.upper().eq("BENIGN")]
        attack = df[~labels.str.upper().eq("BENIGN")]
        if len(benign) > benign_per_file:
            benign = benign.sample(benign_per_file, random_state=seed)
        if len(attack) > attack_per_file:
            attack = attack.sample(attack_per_file, random_state=seed)
        part = pd.concat([benign, attack], ignore_index=True)
        part["__source_file"] = path.name
        frames.append(part)
    return pd.concat(frames, ignore_index=True)


def prepare_binary_data(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    label_col = next((c for c in df.columns if c.lower() == "label"), None)
    if label_col is None:
        raise ValueError("Expected a Label column.")
    y = (~df[label_col].astype(str).str.strip().str.upper().eq("BENIGN")).astype("int8")
    source = df.get("__source_file", pd.Series("unknown", index=df.index))
    X = df.drop(columns=[label_col, "__source_file"], errors="ignore")
    X = X.select_dtypes(include=[np.number]).replace([np.inf, -np.inf], np.nan)
    X = X.dropna(axis=1, how="all")
    X = X.loc[:, ~X.columns.duplicated()].astype("float32")
    return X, y, source
