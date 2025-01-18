import pytest
import pandas as pd
import sys
import os
from pandas.testing import assert_frame_equal
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from summarease.summarize_dtypes import summarize_dtypes_table


def test_summarize_dtypes_table():
    # Test Case 1: Standard input with multiple data types
    data = pd.DataFrame({
        'int_col': [1, 2, 3],
        'float_col': [1.1, 2.2, 3.3],
        'str_col': ['a', 'b', 'c'],
        'bool_col': [True, False, True]
    })
    result = summarize_dtypes_table(data)
    expected = pd.DataFrame({
        'DataType': ['int64', 'float64', 'object', 'bool'],
        'Count': [1, 1, 1, 1]
    })
    assert isinstance(result, pd.DataFrame), "The function should return a DataFrame"
    assert_frame_equal(result, expected)

    # Test Case 2: Empty DataFrame
    empty_data = pd.DataFrame()
    result = summarize_dtypes_table(empty_data)
    expected = pd.DataFrame(columns=['DataType', 'Count'])
    assert isinstance(result, pd.DataFrame), "The function should return a DataFrame"
    assert_frame_equal(result, expected, check_dtype=False)

    # Test Case 3: Single column DataFrame
    single_col_data = pd.DataFrame({'col1': [1, 2, 3]})
    result = summarize_dtypes_table(single_col_data)
    expected = pd.DataFrame({'DataType': ['int64'], 'Count': [1]})
    assert isinstance(result, pd.DataFrame), "The function should return a DataFrame"
    assert_frame_equal(result, expected, check_dtype=False)

    # Test Case 4: DataFrame with datetime column
    datetime_data = pd.DataFrame({
        'int_col': [1, 2, 3],
        'datetime_col': pd.date_range("2023-01-01", periods=3)
    })
    result = summarize_dtypes_table(datetime_data)
    expected = pd.DataFrame({
        'DataType': ['int64', 'datetime64[ns]'],
        'Count': [1, 1]
    })
    assert isinstance(result, pd.DataFrame), "The function should return a DataFrame"
    assert_frame_equal(result, expected, check_dtype=False)

    # Test Case 5: Non-DataFrame input (list)
    with pytest.raises(TypeError):
        summarize_dtypes_table([1, 2, 3])

    # Test Case 6: Non-DataFrame input (None)
    with pytest.raises(TypeError):
        summarize_dtypes_table(None)

    # Test Case 7: Mixed data types including NaN
    mixed_data = pd.DataFrame({
        'int_col': [1, 2, None],
        'float_col': [1.1, None, 3.3],
        'str_col': ['a', None, 'c']
    })
    result = summarize_dtypes_table(mixed_data)
    expected = pd.DataFrame({
        'DataType': ['float64', 'object'],
        'Count': [2, 1]
        })
    assert isinstance(result, pd.DataFrame), "The function should return a DataFrame"
    assert_frame_equal(result, expected, check_dtype=False)
