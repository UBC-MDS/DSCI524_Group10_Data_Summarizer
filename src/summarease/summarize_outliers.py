def summarize_outliers(dataset_name, columns=None, summarize_by="table"):
    """Check and summarize the outliers by Z-scores in specified numeric columns of a table.

    Parameters
    ----------
    dataset_name : DataFrame
        The input dataset containing numeric column(s) for outlier check.
    columns : list of str, optional
        A list of column names to check the outliers. 
        Default is None.
        If none, all numeric columns in the table will be checked.
    summarize_by : str, within {"table", "plot", "mix"}, optional
        The method to summarize the outliers:
        "table": Default, returns a summary table showing outliers for each column.
        "plot": Visualizes a boxplot to display outliers.
        "mix": Combines both table and plot.

    Returns
    -------
    dict or None
        If summarize_by="table" or summarize_by="mix", returns a dictionary.
        Keys: column names; values: lists of indices of rows containing outliers.
        If summarize_by="plot", returns None. A plot will be displayed. 

    Notes:
    -----
    Outliers are idenfied with a absolute value of z-score greater than 3.

    Examples
    --------
    >>> summarize_outliers(data, summarize_by="table")
    """
    pass