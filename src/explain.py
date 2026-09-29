from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import shap
from .data import load_research_sample, prepare_binary_data


def explain_random_forest(data_dir, model_path="artifacts/random/random_forest.joblib", sample_size=500):
    """Compute reproducible SHAP importance for the attack class."""
    df = load_research_sample(data_dir, benign_per_file=10000, attack_per_file=10000)
    X, _, _ = prepare_binary_data(df)
    sample = X.sample(min(sample_size, len(X)), random_state=42)
    model = joblib.load(model_path)
    transformed = model.named_steps["imputer"].transform(sample)
    forest = model.named_steps["model"]
    values = shap.TreeExplainer(forest).shap_values(transformed)
    arr = np.asarray(values)
    if isinstance(values, list):
        attack_values = values[1]
    elif arr.ndim == 3:
        attack_values = arr[:, :, 1]
    else:
        attack_values = arr
    importance = np.abs(attack_values).mean(axis=0)
    result = pd.DataFrame({"feature": sample.columns, "mean_abs_shap": importance})
    result = result.sort_values("mean_abs_shap", ascending=False)
    out = Path("artifacts")
    out.mkdir(exist_ok=True)
    result.to_csv(out / "shap_importance.csv", index=False)
    return result
