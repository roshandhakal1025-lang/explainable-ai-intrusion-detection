import pandas as pd
from src.data import prepare_binary_data


def test_prepare_binary_data_creates_binary_target():
    df = pd.DataFrame({
        "Flow Duration": [10, 20, 30],
        "Packets": [1, 2, 3],
        "Label": ["BENIGN", "DoS Hulk", "BENIGN"],
    })
    X, y = prepare_binary_data(df)
    assert list(y) == [0, 1, 0]
    assert "Label" not in X.columns
    assert list(X.columns) == ["Flow Duration", "Packets"]
