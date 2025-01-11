def summarize_missing_values(dataset, summarize_by="table"):
    """
    Summarize the missing values in the dataset, providing information on the number and percentage of 
    missing values for each column. If there are missing values, a summary table or a visualization can 
    be generated depending on the `summarize_by` argument.

    Parameters:
    -----------
        dataset : pd.DataFrame
            The dataset to analyze.
        summarize_by (str): 
            The format for summarizing the missing values. 
                            Options are "table" (default), "plot" or "mixed". If "table", a summary table is 
                            generated showing the count and percentage of missing values for each column. 
                            If "plot", a bar plot will be displayed showing the missing values per column 
                            as a percentage of the total. If "mixed", displays both table and plot.

    Returns:
    -------
        None: Displays either a table or a plot or both, depending on the `summarize_by` argument.

    Notes:
    ------
        - This function only summarizes missing values; it does not handle the imputation or removal of them.
        - The missing values are defined as NaN, None, or similar missing indicators.
    
    Example:
    -------
    >>> summarize_missing_values(dataset=df, summarize_by="table")
    """
