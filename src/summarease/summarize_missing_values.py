def summarize_missing_values(dataset: pd.Dataframe, summarize_by: str = "table"):
    """
    Summarize the missing values in the dataset, providing information on the number and percentage of 
    missing values for each column. Generate a summary table or visualization to show the missing values
    depending on the `summarize_by` argument.

    Parameters:
    -----------
        dataset : pd.DataFrame
            The dataset to analyze.
        summarize_by (str): 
            The format for summarizing the missing values. 
                            Options are "table" (default) or "plot". If "table", a summary table is 
                            generated showing the count and percentage of missing values for each column. 
                            If "plot", a bar plot will be displayed showing the missing values per column 
                            as a percentage of the total.

    Returns:
    -------
        None: Displays either a table or a plot, depending on the `summarize_by` argument.

    Notes:
    ------
        - This function only summarizes missing values; it does not handle the imputation or removal of them.
        - The missing values are defined as NaN, None, or similar missing indicators.
    
    Example:
    -------
    >>> summarize_missing_values(dataset=df, summarize_by="table")
    """
    pass