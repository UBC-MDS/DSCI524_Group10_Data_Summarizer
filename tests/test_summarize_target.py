import pytest
import pandas as pd
from summarease.summarize_target import summarize_target_df

def test_categorical_correct_proportions():
    data = pd.DataFrame({"target": ["x", "y", "z", "x", "y", "y"]})
    result = summarize_target_df(data, "target", "categorical", threshold=0.2)
    expected_proportions = [2/6, 3/6, 1/6]
    assert result["proportion"].tolist() == expected_proportions
    assert (result["threshold"] == 0.2).all()  # Validate threshold column

def test_categorical_class_imbalance():
    data = pd.DataFrame({"target": ["x", "y", "z", "x", "y", "y"]})
    result = summarize_target_df(data, "target", "categorical", threshold=0.2)
    assert result["imbalanced"].tolist() == [False, True, True]
    assert (result["threshold"] == 0.2).all()  # Validate threshold column

def test_categorical_default_threshold():
    data = pd.DataFrame({"target": ["x", "y", "z", "x", "y", "y"]})
    result = summarize_target_df(data, "target", "categorical")
    assert "imbalanced" in result.columns
    assert (result["threshold"] == 0.2).all()

def test_categorical_empty_dataset():
    data = pd.DataFrame({"target": []})
    result = summarize_target_df(data, "target", "categorical", threshold=0.2)
    assert result.empty
    assert "threshold" in result.columns

def test_categorical_missing_column():
    data = pd.DataFrame({"other_column": [1, 2, 3]})
    with pytest.raises(KeyError):
        summarize_target_df(data, "target", "categorical")

def test_numerical_descriptive_statistics():
    data = pd.DataFrame({"target": [1, 2, 3, 4, 5]})
    with pytest.warns(UserWarning, match="Threshold is not used for numerical targets."):
        result = summarize_target_df(data, "target", "numerical", threshold=0.5)
    assert result.loc["target", "mean"] == 3
    assert result.loc["target", "std"] == pytest.approx(1.5811, 0.0001)

def test_categorical_extremely_imbalanced():
    data = pd.DataFrame({"target": ["x"] * 99 + ["y"]})
    result = summarize_target_df(data, "target", "categorical", threshold=0.2)
    assert result["imbalanced"].tolist() == [True, True]

def test_categorical_equal_proportions():
    data = pd.DataFrame({"target": ["x", "y", "z"] * 10})
    result = summarize_target_df(data, "target", "categorical", threshold=0.2)
    assert result["imbalanced"].tolist() == [False, False, False]

def test_numerical_identical_values():
    data = pd.DataFrame({"target": [5, 5, 5, 5, 5]})
    with pytest.warns(UserWarning, match="Threshold is not used for numerical targets."):
        result = summarize_target_df(data, "target", "numerical", threshold=0.5)
    assert result.loc["target", "std"] == 0

def test_numerical_empty_dataset():
    data = pd.DataFrame({"target": []})
    result = summarize_target_df(data, "target", "numerical")
    assert result.empty

def test_invalid_target_type():
    data = pd.DataFrame({"target": [1, 2, 3]})
    with pytest.raises(ValueError):
        summarize_target_df(data, "target", "invalid_type")

def test_numerical_with_threshold_warning():
    data = pd.DataFrame({"target": [1, 2, 3, 4, 5]})
    with pytest.warns(UserWarning, match="Threshold is not used for numerical targets."):
        summarize_target_df(data, "target", "numerical", threshold=0.5)

def test_numerical_large_range():
    data = pd.DataFrame({"target": [1e8, 2e8, 3e8, 4e8, 5e8]})
    with pytest.warns(UserWarning, match="Threshold is not used for numerical targets."):
        result = summarize_target_df(data, "target", "numerical", threshold=0.5)
    assert not result.empty

def test_invalid_threshold():
    data = pd.DataFrame({"target": ["x", "x", "z", "x", "y", "z"]})
    with pytest.raises(ValueError):
        summarize_target_df(data, "target", "categorical", threshold=-0.1)
    with pytest.raises(ValueError):
        summarize_target_df(data, "target", "categorical", threshold=1.5)

def test_numerical_without_threshold():
    data = pd.DataFrame({"target": [1, 2, 3, 4, 5]})
    summarize_target_df(data, "target", "numerical", threshold=None)


