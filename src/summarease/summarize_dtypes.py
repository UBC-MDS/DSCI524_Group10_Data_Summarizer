def summarize_dtypes(dataset: pd.Dataframe, summarize_by: str = "table"):
    """Summarize the data types in the dataset.

    Parameters
    ----------
    dataset : DataFrame
        The input dataset to analyze.
    summarize_by : str, within {"table", "plot"}, optional
        Specifies the output format:
        - "table": Returns a summary as a table.
        - "plot": Visualizes the data type distribution as a plot.
        Default is "table".

    Returns
    -------
    dict or None
        A dictionary containing the data type counts if `summarize_by="table"`.
        If `summarize_by="plot"`, displays a visualization and returns None.

    Notes
    -----
    This function counts the occurrences of each data type in the dataset and
    either generates a summary table or visualizes the distribution using a plot.

    Examples
    --------
    >>> summarize_dtypes(dataset=data, summarize_by="table")
    {'int64': 5, 'float64': 3, 'object': 4}
    
    >>> summarize_dtypes(dataset=data, summarize_by="plot")
    # Displays a bar plot showing the distribution of data types.
    """
    pass