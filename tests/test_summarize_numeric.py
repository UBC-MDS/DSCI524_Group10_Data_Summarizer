import pandas as pd
from summarease.summarize_numeric import summarize_numeric, plot_numeric_density, plot_correlation_heatmap
import pytest
import numpy as np
import altair as alt
from io import StringIO
from unittest.mock import patch


data = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1],
        'C': ['a', 'b', 'c', 'd', 'e']
    })

# Test 1: Dataframe with numerical variables with at least one non-null value
@pytest.fixture
def df_with_numeric_data():
    return pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1],
        'C': ['a', 'b', 'c', 'd', 'e']
    })

def test_summarize_numeric_with_numerical_data(df_with_numeric_data):
    output = summarize_numeric(data, summarize_by="table")
    assert "count" in output["numeric_describe"].index 
    assert "mean" in output["numeric_describe"].index
    assert "std" in output["numeric_describe"].index

# Test 2: Dataframe with one numerical variable with at least one non-null value
@pytest.fixture
def df_with_single_numeric_column():
    return pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': ['a', 'b', 'c', 'd', 'e']
    })

def test_summarize_numeric_with_single_column():
    output = summarize_numeric(data[["A", "C"]], summarize_by="table")
    assert "count" in output["numeric_describe"].index 
    assert "mean" in output["numeric_describe"].index
    assert "std" in output["numeric_describe"].index

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

def test_summarize_numeric_no_numeric_columns():
        output = summarize_numeric(data[["C"]], summarize_by="table")
        assert output is None

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


# Test 7: Erroneous/Adversarial Input. First argument not a dataframe
def test_summarize_numeric_invalid_first_argument():
    with pytest.raises(AssertionError):
        summarize_numeric("not a dataframe", summarize_by="table")

# Test 8: Erroneous/Adversarial Input. Second argument invalid
def test_summarize_numeric_invalid_summarize_by():
    with pytest.raises(AssertionError):
        summarize_numeric(pd.DataFrame({'A': [1, 2, 3]}), summarize_by="invalid")

def test_valid_dataframe():
    # Test with a valid DataFrame of numeric values
    data = {'A': [1, 2, 3, 4, 5], 'B': [5, 6, 7, 8, 9]}
    df = pd.DataFrame(data)
    
    result = plot_numeric_density(df)
    
    assert isinstance(result, alt.vegalite.v5.api.VConcatChart)


def test_invalid_input_type():
    # Test with an invalid input type (e.g., list instead of a DataFrame)
    invalid_input = [1, 2, 3, 4, 5]
    
    with pytest.raises(AssertionError):
        plot_numeric_density(invalid_input)


def test_empty_dataframe():
    # Test with an empty DataFrame
    empty_df = pd.DataFrame()
    
    result = plot_numeric_density(empty_df)
    
    assert isinstance(result, alt.vegalite.v5.api.VConcatChart)
    assert len(result.to_dict()["vconcat"]) == 0  


def test_single_column_dataframe():
    # Test with a DataFrame containing only one numeric column
    data = {'A': [1, 2, 3, 4, 5]}
    df = pd.DataFrame(data)
    
    result = plot_numeric_density(df)
    
    assert isinstance(result, alt.vegalite.v5.api.VConcatChart)
    assert len(result.to_dict()['data']) > 0


def test_large_dataframe():
    # Test with a very large DataFrame
    data = {'A': range(1000), 'B': range(1000, 2000)}
    df = pd.DataFrame(data)
    
    result = plot_numeric_density(df)
    
    assert isinstance(result, alt.vegalite.v5.api.VConcatChart)
    assert len(result.to_dict()['data']) > 0


def test_numeric_column_with_zeros():
    # Test with a column containing zero values
    data = {'A': [0, 0, 0, 0, 0], 'B': [1, 2, 3, 4, 5]}
    df = pd.DataFrame(data)
    
    result = plot_numeric_density(df)
    
    assert isinstance(result, alt.vegalite.v5.api.VConcatChart)
    assert len(result.to_dict()['data']) > 0


def test_dataframe_input():
    with pytest.raises(AssertionError):
        plot_correlation_heatmap([1, 2, 3])

def test_properties():
    # Check chart properties
    data = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [2, 3, 4, 5, 6],
        'C': [5, 4, 3, 2, 1]
    })
    chart = plot_correlation_heatmap(data)
    
    
    assert chart.width == 400
    assert chart.height == 400

def test_encoding():
    data = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [2, 3, 4, 5, 6],
        'C': [5, 4, 3, 2, 1]
    })
    chart = plot_correlation_heatmap(data)
    layer_1, layer_2 = chart.layer

    assert layer_1.encoding.x.shorthand == 'Var1:N'
    assert layer_1.encoding.y.shorthand == 'Var2:N'
    assert layer_1.encoding.color.shorthand == 'Correlation:Q'
    
    assert layer_2.encoding.x.shorthand == 'Var1:N'
    assert layer_2.encoding.y.shorthand == 'Var2:N'
    assert layer_2.encoding.text.shorthand == 'Correlation:Q'

