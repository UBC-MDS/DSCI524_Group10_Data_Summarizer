import pandas as pd
from summarease.summarize_numeric import summarize_numeric
import pytest

from io import StringIO
from unittest.mock import patch

# Test 1: Dataframe with numerical variables with at least one non-null value
@pytest.fixture
def df_with_numeric_data():
    return pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1],
        'C': ['a', 'b', 'c', 'd', 'e']
    })

def test_summarize_numeric_with_numerical_data(df_with_numeric_data):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        summarize_numeric(df_with_numeric_data, summarize_by="table")
        output = mock_stdout.getvalue()
        assert "count" in output  # Check if summary statistics are printed
        assert "mean" in output
        assert "std" in output

# Test 2: Dataframe with one numerical variable with at least one non-null value
@pytest.fixture
def df_with_single_numeric_column():
    return pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': ['a', 'b', 'c', 'd', 'e']
    })

def test_summarize_numeric_with_single_column(df_with_single_numeric_column):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        summarize_numeric(df_with_single_numeric_column, summarize_by="table")
        output = mock_stdout.getvalue()
        assert "count" in output
        assert "mean" in output
        assert "std" in output

# Test 3: Second argument is one of the accepted enumerations
def test_summarize_numeric_with_valid_summarize_by():
    valid_args = ["table", "plot"]
    for arg in valid_args:
        result = summarize_numeric(pd.DataFrame({'A': [1, 2, 3]}), summarize_by=arg)
        assert result is not None  # Ensure it completes without error

# Test 4: Dataframe with no numerical variables
@pytest.fixture
def df_with_no_numeric_columns():
    return pd.DataFrame({
        'A': ['a', 'b', 'c', 'd', 'e'],
        'B': ['f', 'g', 'h', 'i', 'j']
    })

def test_summarize_numeric_no_numeric_columns(df_with_no_numeric_columns):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        summarize_numeric(df_with_no_numeric_columns, summarize_by="table")
        output = mock_stdout.getvalue()
        assert "No numeric columns found in the dataset." in output

# Test 5: Dataframe with a numerical variable that contains all null values
@pytest.fixture
def df_with_all_null_numeric():
    return pd.DataFrame({
        'A': [None, None, None, None, None],
        'B': ['f', 'g', 'h', 'i', 'j']
    })

def test_summarize_numeric_with_all_null_values(df_with_all_null_numeric):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        summarize_numeric(df_with_all_null_numeric, summarize_by="table")
        output = mock_stdout.getvalue()
        assert "count" not in output  # Check that no summary stats are printed
        assert "mean" not in output

# Test 6: Too few data to create plot
@pytest.fixture
def df_with_too_few_data():
    return pd.DataFrame({
        'A': [1],
        'B': [5]
    })

def test_summarize_numeric_too_few_data(df_with_too_few_data):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        result = summarize_numeric(df_with_too_few_data, summarize_by="plot")
        output = mock_stdout.getvalue()
        # Expect no plot output, since there's only one row of data
        assert "numeric_plot" not in result

# Test 7: Erroneous/Adversarial Input. First argument not a dataframe
def test_summarize_numeric_invalid_first_argument():
    with pytest.raises(AssertionError):
        summarize_numeric("not a dataframe", summarize_by="table")

# Test 8: Erroneous/Adversarial Input. Second argument invalid
def test_summarize_numeric_invalid_summarize_by():
    with pytest.raises(AssertionError):
        summarize_numeric(pd.DataFrame({'A': [1, 2, 3]}), summarize_by="invalid")