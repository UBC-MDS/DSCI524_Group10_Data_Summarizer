import pandas as pd
from summarease.summarize_numeric import summarize_numeric
import pytest

from io import StringIO
from unittest.mock import patch

@pytest.fixture
def df_with_numeric_data():
    """Fixture to create a DataFrame with numeric data."""
    data = {
        "A": [1, 2, 3, 4, 5],
        "B": ["a", "b", "c", "d", "e"],
        "C": [5, 4, 3, 2, 1]
    }
    return pd.DataFrame(data)

@pytest.fixture
def df_with_single_numeric_column():
    """Fixture to create a DataFrame with a single numeric column."""
    data = {
        "A": [1, 2, 3, 4, 5],
    }
    return pd.DataFrame(data)

@pytest.fixture
def df_with_no_numeric_columns():
    """Fixture to create a DataFrame with no numeric columns."""
    data = {
        "A": ["a", "b", "c", "d", "e"],
        "B": ["f", "g", "h", "i", "j"]
    }
    return pd.DataFrame(data)

@pytest.fixture
def df_with_end_categorical_column():
    """Fixture to create a DataFrame with categorical data column at an end."""
    data = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
    return pd.DataFrame(data)

# Test case 0: Test summarize_numeric with default summarize_by argument ("table")
def test_summarize_numeric_default(df_with_numeric_data):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        summarize_numeric(df_with_numeric_data)
        output = mock_stdout.getvalue()
        # Check if summary statistics were printed (like mean, std, etc.)
        assert "mean" in output
        assert "std" in output
        assert "min" in output
        assert "max" in output

# Test case 1: Test summarize_numeric with summarize_by="table"
def test_summarize_numeric_table(df_with_numeric_data):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        summarize_numeric(df_with_numeric_data, summarize_by="table")
        output = mock_stdout.getvalue()
        # Check if summary statistics were printed (like mean, std, etc.)
        assert "mean" in output
        assert "std" in output
        assert "min" in output
        assert "max" in output

# Test case 3: Test invalid summarize_by value
def test_summarize_numeric_invalid_option(df_with_numeric_data):
    with pytest.raises(ValueError):
        summarize_numeric(df_with_numeric_data, summarize_by="invalid_option")

# Test case 4: Test summarize_numeric with no numeric columns in the dataset
def test_summarize_numeric_no_numeric_columns(df_with_no_numeric_columns):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        summarize_numeric(df_with_no_numeric_columns, summarize_by="table")
        output = mock_stdout.getvalue()
        assert "No numeric columns found in the dataset." in output

# Test case 5: Test summarize_numeric with a single numeric column
def test_summarize_numeric_single_column(df_with_single_numeric_column):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        summarize_numeric(df_with_single_numeric_column, summarize_by="table")
        output = mock_stdout.getvalue()
        # Ensure we get summary stats for the single column
        assert "mean" in output
        assert "std" in output
        assert "min" in output
        assert "max" in output