import pandas as pd
def summarize_numeric(dataset: pd.DataFrame, summarize_by: str = "table"):
    """
    Summarize the numeric variables in the dataset by providing the summary statistics (e.g., mean, 
    standard deviation, min, max, etc.) for each numeric column or plotting the correlation heatmap 
    to visualize the relationships between numeric variables. The summary type provided is 
    requested based on the `summarize_by` argument.

    Parameters:
    ----------
        dataset : pd.DataFrame
            The dataset to analyze.
        summarize_by (str): 
            The format for summarizing the numeric variables. 
                            Options are "table" (default) or "plot". If "table", a summary table is 
                            generated with statistics for each numeric column. If "plot", a correlation 
                            heatmap is displayed to visualize the correlation between numeric variables.

    Returns:
    -------
        None: Displays either a table of summary statistics or a plot (correlation heatmap), depending on the 
              `summarize_by` argument.

    Notes:
    ------
        - The correlation heatmap is only applicable if there are two or more numeric columns in the dataset.
        - The summary statistics for numeric columns are computed using `df.describe()`, and additional details 
          (such as count, mean, standard deviation, min, max, etc.) will be included.

    Example:
    -------
    >>> summarize_numeric(dataset=df, summarize_by="table")
    """
    numeric_columns = dataset.select_dtypes(include='number').columns

    if numeric_columns.empty:  # Check if there are no numeric columns
        print("No numeric columns found in the dataset.")
        return
    
    if summarize_by == "table":
        # Generate summary statistics for numeric columns
        summary = dataset[numeric_columns].describe()
        print(summary)
    
    elif summarize_by == "plot":
        # Generate a correlation heatmap for numeric columns
        plot_correlation_heatmap(dataset, numeric_columns)
    
    else:
        raise ValueError(f"Invalid value for summarize_by: {summarize_by}. Expected 'table' or 'plot'.")