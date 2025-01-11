def summarize_numeric(dataset, summarize_by="table"):
    """
    Summarize the numeric variables in the dataset by providing the summary statistics (e.g., mean, 
    standard deviation, min, max, etc.) for each numeric column or plotting the correlation heatmap 
    to visualize the relationships between numeric variables or both. The summary type provided is 
    requested based on the `summarize_by` argument.

    Parameters:
    ----------
        dataset : pd.DataFrame
            The dataset to analyze.
        summarize_by (str): 
            The format for summarizing the numeric variables. 
                            Options are "table" (default), "plot", or "mixed". If "table", a summary table is 
                            generated with statistics for each numeric column. If "plot", a correlation 
                            heatmap is displayed to visualize the correlation between numeric variables.
                            If "mixed", displays both table and heatmap.

    Returns:
    -------
        None: Displays either a table of summary statistics or a plot (correlation heatmap) or both, 
              depending on the `summarize_by` argument.

    Notes:
    ------
        - The correlation heatmap is only applicable if there are two or more numeric columns in the dataset.
        - The summary statistics for numeric columns are computed using `df.describe()`, and additional details 
          (such as count, mean, standard deviation, min, max, etc.) will be included.

    Example:
    -------
    >>> summarize_numeric(dataset=df, summarize_by="table")
    """
    pass