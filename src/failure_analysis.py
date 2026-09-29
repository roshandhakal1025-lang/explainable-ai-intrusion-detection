"""Attack-family failure analysis for the Friday holdout.

Run after preparing the same deterministic development sample used by train.py.
Reports detection rate by original CICIDS2017 label rather than hiding failures
inside one binary aggregate metric.
"""
import pandas as pd
from sklearn.metrics import confusion_matrix


def family_detection_table(labels, y_true, y_pred):
    frame = pd.DataFrame({"label": labels, "actual": y_true, "pred": y_pred})
    rows = []
    for label, group in frame.groupby("label"):
        rows.append({
            "label": label,
            "n": int(len(group)),
            "predicted_attack_rate": float(group["pred"].mean()),
            "correct_rate": float((group["pred"] == group["actual"]).mean()),
        })
    return pd.DataFrame(rows).sort_values("label")
