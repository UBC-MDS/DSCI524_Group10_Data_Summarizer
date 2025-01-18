def summarize_categorical(dataset: pd.DataFrame, summarize_by: str = "table"):
    """
    Summarize the categorical variables in the dataset by providing the number of unique categories
    for each categorical column. If any categorical columns have too many unique categories, a warning 
    is issued.

    Parameters:
    -----------
        dataset : pd.DataFrame
            The dataset to analyze.
        summarize_by (str): 
            The format for summarizing the categorical variables. 
                            Options are "table" (default) or "plot". If "table", a summary table is 
                            generated with the counts of unique categories for each categorical column. 
                            If "plot", a bar plot will be displayed for each categorical column showing 
                            the frequency of each unique category.

    Returns:
    -------
        None: Displays either a table or a plot, depending on the `summarize_by` argument.

    Notes:
    ------
        If a categorical column has more than a threshold number of unique categories, a warning will 
        be printed to notify the user that the column may be too granular for meaningful analysis.
    
    Example:
    -------
    >>> summarize_categorical(dataset=df, summarize_by="table")
    """
    pass
