import pandas as pd
import warnings

def summarize_target_df(dataset_name, target_variable, target_type, threshold=0.2):
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