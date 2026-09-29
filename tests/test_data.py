import pandas as pd
from src.data import prepare_binary_data
from src.train import split_data


def test_prepare_binary_data_creates_binary_target():
    df = pd.DataFrame({"Flow Duration":[10,20,30],"Packets":[1,2,3],"Label":["BENIGN","DoS Hulk","BENIGN"],"__source_file":["Monday.csv","Friday.csv","Monday.csv"]})
    X, y, source = prepare_binary_data(df)
    assert list(y) == [0,1,0]
    assert "Label" not in X.columns
    assert list(source) == ["Monday.csv","Friday.csv","Monday.csv"]


def test_day_aware_split_holds_out_friday():
    X=pd.DataFrame({"x":[1,2,3,4]}); y=pd.Series([0,1,0,1]); source=pd.Series(["Monday.csv","Tuesday.csv","Friday-A.csv","Friday-B.csv"])
    X_train,X_test,y_train,y_test=split_data(X,y,source,"day-aware")
    assert list(X_train["x"]) == [1,2]
    assert list(X_test["x"]) == [3,4]
