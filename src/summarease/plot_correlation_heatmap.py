import pandas as pd

def plot_correlation_heatmap(dataset: pd.Dataframe, numeric_columns: list = None, 
                             save_path: str = None):
    """
    Generate and save a correlation heatmap for the specified numeric columns in a dataset.

    Parameters:
    ----------
    dataset : pd.DataFrame
        The input dataset containing the data for the heatmap.
    
    numeric_columns : list of str, optional
        A list of column names to include in the correlation heatmap. If None, all numeric columns in the dataset will be used.
    
    save_path : str, optional
        File path to save the generated heatmap. If None, the plot will not be saved.

    Returns:
    -------
    None
        Displays the correlation heatmap or optionally saves it to the specified location.

    Example:
    -------
    >>> plot_correlation_heatmap(dataset=df, numeric_columns=["col1", "col2", "col3"], save_path="heatmap.png")
    """
    pass