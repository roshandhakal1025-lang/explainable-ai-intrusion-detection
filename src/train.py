import argparse
from pathlib import Path
import json
import joblib
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, average_precision_score
from .data import load_csv_directory, prepare_binary_data


def evaluate(name, model, X_test, y_test):
    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:, 1]
    cm = confusion_matrix(y_test, pred)
    tn, fp, fn, tp = cm.ravel()
    return {"model": name, "roc_auc": float(roc_auc_score(y_test, prob)), "pr_auc": float(average_precision_score(y_test, prob)), "false_positive_rate": float(fp/(fp+tn)) if (fp+tn) else None, "confusion_matrix": cm.tolist(), "classification_report": classification_report(y_test, pred, output_dict=True, zero_division=0)}


def split_data(X, y, source, strategy):
    if strategy == "random":
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        return X_train, X_test, y_train, y_test
    test_mask = source.str.contains("Friday", case=False, na=False)
    if not test_mask.any() or test_mask.all():
        raise ValueError("Day-aware split requires source filenames containing 'Friday'.")
    return X.loc[~test_mask], X.loc[test_mask], y.loc[~test_mask], y.loc[test_mask]


def build_models():
    return {
        "logistic_regression": Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler()), ("model", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))]),
        "random_forest": Pipeline([("imputer", SimpleImputer(strategy="median")), ("model", RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1, class_weight="balanced_subsample"))]),
    }


def main(data_dir, split_strategy):
    df = load_csv_directory(data_dir)
    X, y, source = prepare_binary_data(df)
    X_train, X_test, y_train, y_test = split_data(X, y, source, split_strategy)
    out = Path("artifacts") / split_strategy
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for name, model in build_models().items():
        model.fit(X_train, y_train)
        results.append(evaluate(name, model, X_test, y_test))
        joblib.dump(model, out / f"{name}.joblib")
    metadata = {"split_strategy": split_strategy, "train_rows": len(X_train), "test_rows": len(X_test), "features": X.shape[1], "attack_prevalence_train": float(y_train.mean()), "attack_prevalence_test": float(y_test.mean()), "results": results}
    (out / "metrics.json").write_text(json.dumps(metadata, indent=2))
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--split-strategy", choices=["random", "day-aware"], default="random")
    args = parser.parse_args()
    main(args.data_dir, args.split_strategy)
