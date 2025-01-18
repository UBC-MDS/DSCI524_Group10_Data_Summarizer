import pandas as pd
import altair as alt

def plot_numeric_density(dataset_numeric):
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


def plot_correlation_heatmap(dataset_numeric):
    assert isinstance(dataset_numeric, pd.DataFrame), f"Argument 'dataset_numeric' should be pandas dataframe (pd.DataFrame)! You have {type(dataset_numeric)}."
    # Calculate the correlations
    corr = dataset_numeric.corr()

    # Melt the correlation matrix into long-form
    corr_melted = corr.reset_index().melt(id_vars='index')
    corr_melted.columns = ['Var1', 'Var2', 'Correlation']
    
    heatmap = alt.Chart(corr_melted).mark_rect().encode(
        x='Var1:N',
        y='Var2:N',
        color='Correlation:Q',
        tooltip=['Var1:N', 'Var2:N', 'Correlation:Q']
    ).properties(
        width=400,
        height=400
    )

    return heatmap


def summarize_numeric(dataset, summarize_by="table"):
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

    outputs = {}

    if (summarize_by == "plot"):
        outputs["numeric_plot"] = plot_numeric_density(dataset_numeric)
        
        if (dataset_numeric.shape[1] > 1):
            outputs["corr_plot"] = plot_correlation_heatmap(dataset_numeric)

    elif (summarize_by == "table"):
        outputs["numeric_describe"] = dataset_numeric.describe()
        
    return outputs