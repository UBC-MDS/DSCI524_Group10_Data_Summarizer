# summarease

A package that provides quick summaries of datasets, including data types, missing value counts, and basic statistics.

## Project Summary

Summarease is a package designed to provide quick insights into a dataset by summarizing its key features. It offers functions that help users understand the structure of the data, making it easier to plan data cleaning and exploratory data analysis (EDA) tasks.

## Package Features

`clean_data`: 
    Clean the input dataset by standardizing column names, replacing invalid values, and ensuring proper data types.

`summarize_dtypes`: 
    Summarize the data types in the dataset.

`summarize_missing_values`: 
    Summarize the missing values in the dataset, providing information on the number and percentage of missing values for each column. Generate a summary table or visualization to show the missing values based on user's choice.

`summarize_outliers`: 
    Check and summarize the outliers by Z-scores in specified numeric columns of a table. Generate a summary table or visualization based on user's choice.

`summarize_target`: 
    Summarize and evaluate the target variable for categarical or numerical types. Generate a summary table or visualization based on target's type.

`summarize_categorical`: 
    Summarize the categorical variables in the dataset by providing the number of unique categories for each categorical column. If any categorical columns have too many unique categories, a warning is issued.

`summarize_numeric`: 
    Summarize the numeric variables in the dataset by providing the summary statistics (e.g., mean, standard deviation, min, max, etc.) for each numeric column or plotting the correlation heatmap to visualize the relationships between numeric variables. Generate a summary table or visualization based on user's choice.

`plot_correlation_heatmap`: 
    Generate and save a correlation heatmap for the specified numeric columns in a dataset.

`summarize`: 
    Summarizes the given dataset by generating various statistics, visualizations, and/or tables based on the provided options.

## Fit Within Python Ecosystem

Summarease is a lightweight and compact Python package designed for efficiency and ease of use. Despite its simplicity, it offers users great flexibility to customize the output format, whether through detailed tables or insightful visualizations.

Related packages with similar functionalities:
sweetviz: https://github.com/fbdesignpro/sweetviz
ydata-profiling: https://github.com/ydataai/ydata-profiling
dtale: https://github.com/man-group/dtale

## Installation

```bash
$ pip install summarease
```

## Usage

```python
from summarease.clean_data import clean_data
from summarease.summarize_dtypes import summarize_dtypes
from summarease.summarize_missing_values import summarize_missing_values
from summarease.summarize_outliers import summarize_outliers
from summarease.summarize_target import summarize_target
from summarease.summarize_categorical import summarize_categorical
from summarease.summarize_numeric import summarize_numeric
from summarease.plot_correlation_heatmap import plot_correlation_heatmap
from summarease.summarize import summarize
import matplotlib.pyplot as plt
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`summarease` is licensed under the terms of the MIT license.

## Contributors

`summarease` was created by Hrayr Muradyan, Yun Zhou, Stephanie Wu, Zuer Zhong

## Credits

`summarease` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
