import pandas as pd
import altair as alt

def plot_numeric_density(dataset_numeric: pd.DataFrame):
    """
    Generate density plots for each numeric column in the provided dataset. Each plot represents the 
    distribution of values in a numeric column using a density estimate.

    Parameters:
    ----------
    dataset_numeric : pd.DataFrame
        A pandas DataFrame containing numeric columns. The function will generate a density plot for 
        each numeric column in the dataset.

    Returns:
    -------
    alt.Chart
        An Altair chart object representing a vertical concatenation of density plots for each numeric column. 
        The plots are grouped into rows with a maximum of 4 plots per row.

    Example:
    -------
    >>> plot_numeric_density(dataset_numeric=df)
    """
    assert isinstance(dataset_numeric, pd.DataFrame), f"Argument 'dataset_numeric' should be pandas dataframe (pd.DataFrame)! You have {type(dataset_numeric)}."

    plots = []
    for col in dataset_numeric.columns:
        plot = alt.Chart(dataset_numeric).transform_density(
            col, as_=['value', 'density']
        ).mark_line().encode(
            x='value:Q',
            y='density:Q',
            color=alt.value('steelblue')
        ).properties(
            title=col
        )
        plots.append(plot)

    # Combine the plots in 3 columns (group the plots into 3)
    n_cols = 4
    n_rows = (len(plots) + n_cols - 1) // n_cols  

    # Divide the plots into rows of 3 columns
    rows = [alt.hconcat(*plots[i:i + n_cols]) for i in range(0, len(plots), n_cols)]

    # Concatenate rows vertically
    final_plot = alt.vconcat(*rows)
    
    return final_plot

def plot_correlation_heatmap(dataset_numeric: pd.DataFrame):
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
    assert isinstance(dataset_numeric, pd.DataFrame), f"Argument 'dataset_numeric' should be pandas dataframe (pd.DataFrame)! You have {type(dataset_numeric)}."
    # Calculate the correlations
    corr = dataset_numeric.corr() 
    # Melt the correlation matrix into long-form
    corr_melted = corr.reset_index().melt(id_vars='index')
    corr_melted.columns = ['Var1', 'Var2', 'Correlation']

    # Round the correlation values to 2 decimal places
    corr_melted['Correlation'] = corr_melted['Correlation'].round(2)
    
    # Create the heatmap with correlation values

    heatmap = alt.Chart(corr_melted).mark_rect().encode(
        x='Var1:N',
        y='Var2:N',
        color='Correlation:Q',
        tooltip=['Var1:N', 'Var2:N', 'Correlation:Q']
    ).properties(
        width=400,
        height=400
    )
    
    # Add correlation value labels on the heatmap cells
    text = alt.Chart(corr_melted).mark_text(dy=-5).encode(
        x='Var1:N',
        y='Var2:N',
        text='Correlation:Q'
    )

    # Overlay the text on top of the heatmap
    return heatmap + text

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
        A table of summary statistics or a plot (correlation heatmap), depending on the 
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
    assert isinstance(dataset, pd.DataFrame), f"Argument 'dataset' should be pandas dataframe (pd.DataFrame)! You have {type(dataset)}."
    assert isinstance(summarize_by, str), f"Argument 'summarize_by' should be a string (str)! You have {type(summarize_by)}."

    # Lower the summarize by
    summarize_by = summarize_by.lower()

    assert summarize_by in {"table", "plot"}, f"Argument 'summarize_by' should be one of the following options: [table, plot]! You have {summarize_by}."
    
    # Select the numeric columns from the dataset
    dataset_numeric = dataset.select_dtypes(include=['number'])

    if dataset_numeric.empty:
        return

    outputs = {}

    if (summarize_by == "plot"):
        outputs["numeric_plot"] = plot_numeric_density(dataset_numeric)
        
        if (dataset_numeric.shape[1] > 1):
            outputs["corr_plot"] = plot_correlation_heatmap(dataset_numeric)

    elif (summarize_by == "table"):
        outputs["numeric_describe"] = dataset_numeric.describe()
        
    return outputs