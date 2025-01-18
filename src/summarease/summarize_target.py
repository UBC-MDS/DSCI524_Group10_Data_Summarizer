import pandas as pd
import altair as alt
import warnings

def summarize_target_df(dataset_name: pd.DataFrame, target_variable: str, 
                     target_type: str, threshold=0.2):
    """Summarize and evaluate the target variable for categarical or numerical types.

    Parameters
    ----------
    dataset_name : DataFrame
        The input dataset containing target variable.
    target_variable : str
        The name of target column.
    target_type : str, within {"categorical", "numerical"}
        The type of target variable.
    threshold : float, optional
        Only feasible for "categorical" type to identify class imbalance.
        Default is 0.2.

    Returns
    -------
    DataFrame
        If target_type="categorical", returns a summary DataFrame 
            containing classes, proportions, imbalance flag,
            and threshold.
        If target_type="numerical", returns the DataFrame with the basic 
            statistical summary. 

    Notes:
    -----
    For categorical type, the function does not distinguish between binary and 
        multi-class classification.
    Balance criteria: Assume n classes, each class should between 
        [(1-threshold)/n, (1+threshold)/n].
    threshold : float, optional
        Only used if `target_type="categorical"`. 
        It identifies class imbalance.

    Examples
    --------
    >>> summarize_target(
    data, target_variable='target', target_type='categorical', threshold=0.2
    )
    """
    if target_type == "categorical" and (threshold < 0 or threshold > 1):
        raise ValueError("Threshold must be between 0 and 1.")
    
    if target_type == "categorical":
        # Calculate class proportions
        value_counts = dataset_name[target_variable].value_counts(normalize=True).sort_index()
        n_classes = len(value_counts)

        # Deal with empty data
        if n_classes == 0:
            return pd.DataFrame(columns=['class', 'proportion', 'imbalanced', 'threshold'])

        # Calculate expected range for balance
        expected_proportion = 1 / n_classes
        lower_bound = expected_proportion * (1 - threshold)
        upper_bound = expected_proportion * (1 + threshold)
        imbalance_flag = (value_counts < lower_bound) | (value_counts > upper_bound)

        # Generate summary table
        summary_df = pd.DataFrame({
            'class': value_counts.index,
            'proportion': value_counts.values,
            'imbalanced': imbalance_flag.values
        })
        summary_df['threshold'] = threshold

    elif target_type == "numerical":
        # Check for empty numerical data
        if dataset_name[target_variable].empty:
            return pd.DataFrame()

        # Warn if threshold is provided
        if threshold is not None:
            warnings.warn("Threshold is not used for numerical targets.", UserWarning)

        # Get statistical summary
        summary_df = dataset_name[target_variable].describe().to_frame().T

    else:
        raise ValueError("Invalid target_type. Must be 'categorical' or 'numerical'.")

    return summary_df



def summarize_target_balance_plot(summary_df: pd.DataFrame):
    """
    Visualize the balance condition of a categorical target.

    Parameters
    ----------
    summary_df : DataFrame
        The input DataFrame, expected to match the output of summarize_target_df()
        with target_type="categorical".
        It must contain the columns ['class', 'proportion', 'imbalanced', 'threshold'].

    Returns
    -------
    alt.Chart
        The Altair chart visualizing the balance of the categorical target variable.

    Notes
    -----
    The chart includes the following:
        - A bar plot for actual class proportions.
        - Expected proportion range (lower and upper bounds) as balance range.
        - Imbalance status for each class indicated by color.
        - Highlighted ticks for expected lower and upper bounds.
    """
    # Validate input DataFrame
    required_columns = {'class', 'proportion', 'imbalanced', 'threshold'}
    if not required_columns.issubset(summary_df.columns):
        raise ValueError(f"Input DataFrame must contain columns: {', '.join(sorted(required_columns))}")

    # Handle empty DataFrame
    if summary_df.empty:
        return alt.Chart(pd.DataFrame()).mark_text().encode(
            text=alt.value("No data available for visualization.")
        ).properties(
            title="Categorical Target Balance Visualization (Empty)"
        )

    # Add expected proportion range to the DataFrame
    n_classes = len(summary_df)
    expected_proportion = 1 / n_classes
    threshold = summary_df['threshold'].iloc[0]
    summary_df['expected_lower'] = expected_proportion * (1 - threshold)
    summary_df['expected_upper'] = expected_proportion * (1 + threshold)

    # Bar chart for actual proportions
    actual_dist = alt.Chart(summary_df).mark_bar(opacity=0.6).encode(
        x=alt.X('class:N', title='Class'),
        y=alt.Y('proportion:Q', title='Proportion'),
        color=alt.Color('imbalanced:N', scale=alt.Scale(domain=[True, False], range=['red', 'green']),
                        legend=alt.Legend(title="Imbalanced")),
        tooltip=['class', 'proportion', 'imbalanced']
    )

    # Error bars for expected range
    error_bar = alt.Chart(summary_df).mark_errorbar(color='black').encode(
        x=alt.X('class:N', title='Class'),
        y=alt.Y('expected_lower:Q', title='Expected Proportion Range'),
        y2='expected_upper:Q'
    )

    # Add ticks to highlight lower and upper bounds
    lower_ticks = alt.Chart(summary_df).mark_tick(
        color='black',
        thickness=2,
        size=20  
    ).encode(
        x=alt.X('class:N', title='Class'),
        y=alt.Y('expected_lower:Q')  
    )

    upper_ticks = alt.Chart(summary_df).mark_tick(
        color='black',
        thickness=2,
        size=20  
    ).encode(
        x=alt.X('class:N'),
        y=alt.Y('expected_upper:Q')  
    )

    balance_chart = (actual_dist + error_bar + lower_ticks + upper_ticks).properties(
        width=600,
        height=400,
        title="Categorical Target Balance Visualization"
    )

    return balance_chart