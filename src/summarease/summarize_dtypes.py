import pandas as pd

def summarize_dtypes_table(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize the data types in the dataset and return a DataFrame.

    Parameters
    ----------
    dataset : DataFrame
        The input dataset to analyze.

    Returns
    -------
    DataFrame
        A DataFrame summarizing the counts of each data type.

    Raises
    ------
    TypeError
        If the input dataset is not a pandas DataFrame.

    Examples
    --------
    >>> data = pd.DataFrame({
    ...     'int_col': [1, 2, 3],
    ...     'float_col': [1.1, 2.2, 3.3],
    ...     'str_col': ['a', 'b', 'c'],
    ...     'bool_col': [True, False, True]
    ... })
    >>> summarize_dtypes_table(data)
       DataType  Count
    0    int64      1
    1  float64      1
    2   object      1
    3     bool      1
    """
    if not isinstance(dataset, pd.DataFrame):
        raise TypeError("The input dataset must be a pandas DataFrame.")
    
    # Get data types and their counts
    dtype_counts = dataset.dtypes.value_counts().reset_index()
    dtype_counts.columns = ['DataType', 'Count']

    # Convert DataType column to string for consistent output
    dtype_counts['DataType'] = dtype_counts['DataType'].astype(str)

    return dtype_counts
