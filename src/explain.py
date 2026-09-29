from pathlib import Path
import joblib
import shap
from .data import load_csv_directory, prepare_binary_data


def explain_random_forest(data_dir, model_path="artifacts/random_forest.joblib", sample_size=500):
    df = load_csv_directory(data_dir)
    X, _ = prepare_binary_data(df)
    model = joblib.load(model_path)
    sample = X.sample(min(sample_size, len(X)), random_state=42)
    imputer = model.named_steps["imputer"]
    forest = model.named_steps["model"]
    transformed = imputer.transform(sample)
    explainer = shap.TreeExplainer(forest)
    values = explainer.shap_values(transformed)
    Path("artifacts").mkdir(exist_ok=True)
    return values, sample.columns.tolist()
