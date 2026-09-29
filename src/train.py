import argparse
from pathlib import Path
import json
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from .data import load_csv_directory, prepare_binary_data


def evaluate(name, model, X_test, y_test):
    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:, 1]
    return {
        "model": name,
        "roc_auc": float(roc_auc_score(y_test, prob)),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
        "classification_report": classification_report(y_test, pred, output_dict=True),
    }


def main(data_dir):
    df = load_csv_directory(data_dir)
    X, y = prepare_binary_data(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    logistic = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])
    forest = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("model", RandomForestClassifier(
            n_estimators=200, random_state=42, n_jobs=-1, class_weight="balanced"
        )),
    ])

    models = {"logistic_regression": logistic, "random_forest": forest}
    results = []
    out = Path("artifacts")
    out.mkdir(exist_ok=True)
    for name, model in models.items():
        model.fit(X_train, y_train)
        results.append(evaluate(name, model, X_test, y_test))
        joblib.dump(model, out / f"{name}.joblib")

    (out / "metrics.json").write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True)
    args = parser.parse_args()
    main(args.data_dir)
