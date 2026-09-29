"""Validation-selected threshold experiment for Friday generalization."""
import numpy as np
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

def choose_threshold(y_val, probabilities, max_fpr=0.01):
    rows=[]
    for threshold in np.linspace(0.01,0.99,99):
        pred=(probabilities>=threshold).astype(int)
        tn,fp,fn,tp=confusion_matrix(y_val,pred).ravel()
        fpr=fp/(fp+tn)
        rows.append({"threshold":float(threshold),
          "precision":float(precision_score(y_val,pred,zero_division=0)),
          "recall":float(recall_score(y_val,pred)),
          "f1":float(f1_score(y_val,pred)),"fpr":float(fpr)})
    eligible=[r for r in rows if r["fpr"]<=max_fpr]
    if not eligible: raise ValueError("No threshold satisfies max_fpr")
    return max(eligible,key=lambda r:(r["recall"],r["f1"],-r["fpr"]))
