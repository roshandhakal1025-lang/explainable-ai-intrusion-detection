import argparse, json
from pathlib import Path
import joblib
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, average_precision_score
from .data import load_research_sample, prepare_binary_data


def evaluate(name, model, X_test, y_test):
    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:, 1]
    cm = confusion_matrix(y_test, pred)
    tn, fp, fn, tp = cm.ravel()
    return {"model": name, "roc_auc": float(roc_auc_score(y_test, prob)),
            "pr_auc": float(average_precision_score(y_test, prob)),
            "false_positive_rate": float(fp/(fp+tn)) if fp+tn else None,
            "confusion_matrix": cm.tolist(),
            "classification_report": classification_report(y_test, pred, output_dict=True, zero_division=0)}


def split_data(X, y, source, strategy):
    if strategy == "random":
        return train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
    mask = source.str.contains("Friday", case=False, na=False)
    if not mask.any() or mask.all():
        raise ValueError("Day-aware split requires original Friday filenames.")
    return X.loc[~mask], X.loc[mask], y.loc[~mask], y.loc[mask]


def build_models():
    return {
      "logistic_regression": Pipeline([("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()), ("model", LogisticRegression(max_iter=1000,class_weight="balanced",random_state=42))]),
      "random_forest": Pipeline([("imputer", SimpleImputer(strategy="median")),
        ("model", RandomForestClassifier(n_estimators=120,max_depth=20,min_samples_leaf=2,n_jobs=-1,class_weight="balanced_subsample",random_state=42))])
    }


def main(data_dir, split_strategy, benign_per_file, attack_per_file):
    df = load_research_sample(data_dir, benign_per_file, attack_per_file)
    X,y,source = prepare_binary_data(df)
    X_train,X_test,y_train,y_test = split_data(X,y,source,split_strategy)
    out=Path("artifacts")/split_strategy; out.mkdir(parents=True,exist_ok=True)
    results=[]
    for name,model in build_models().items():
        model.fit(X_train,y_train); results.append(evaluate(name,model,X_test,y_test))
        joblib.dump(model,out/f"{name}.joblib")
    meta={"sampling":{"benign_per_file":benign_per_file,"attack_per_file":attack_per_file,"seed":42},
          "split_strategy":split_strategy,"sample_rows":len(X),"train_rows":len(X_train),"test_rows":len(X_test),
          "features":X.shape[1],"attack_prevalence_train":float(y_train.mean()),"attack_prevalence_test":float(y_test.mean()),
          "results":results}
    (out/"metrics.json").write_text(json.dumps(meta,indent=2)); print(json.dumps(meta,indent=2))


if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--data-dir",required=True)
    p.add_argument("--split-strategy",choices=["random","day-aware"],default="random")
    p.add_argument("--benign-per-file",type=int,default=25000); p.add_argument("--attack-per-file",type=int,default=25000)
    a=p.parse_args(); main(a.data_dir,a.split_strategy,a.benign_per_file,a.attack_per_file)
