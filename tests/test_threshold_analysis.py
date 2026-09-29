import numpy as np
import pandas as pd
from src.threshold_analysis import choose_threshold

def test_threshold_selection_respects_validation_fpr_cap():
    y=pd.Series([0,0,0,0,1,1,1,1])
    p=np.array([.01,.02,.03,.04,.60,.70,.80,.90])
    chosen=choose_threshold(y,p,max_fpr=0.01)
    assert chosen["fpr"] <= 0.01
    assert chosen["recall"] == 1.0
