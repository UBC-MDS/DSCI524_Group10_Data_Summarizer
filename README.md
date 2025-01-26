# summarease

## Project Summary

Summarease is a package designed to provide quick insights into a dataset by summarizing its key features. It offers functions that help users understand the structure of the data, making it easier to plan data cleaning and exploratory data analysis (EDA) tasks.

## Package Features

- `summarize_dtypes`:  
  Summarize the data types in the dataset.

- `summarize_target`:  
  Summarize and evaluate the target variable for categorical or numerical types. Generate a summary or proportion table for numerical or categorical target. Generate a visualization for categorical balance check.

- `summarize_numeric`:  
  Summarize the numeric variables in the dataset by providing the summary statistics (e.g., mean, standard deviation, min, max, etc.) for each numeric column or plotting the correlation heatmap to visualize the relationships between numeric variables. Generate density plots for each numeric column in the provided dataset. Generate a correlation heatmap for the specified numeric columns in a dataset.

- `summarize`:  
  Summarize generates a comprehensive PDF report for a dataset, including statistical summaries, visualizations, and target variable analysis. It supports customizable options like sample observations, automatic data cleaning, and flexible summarization methods (tables, plots, or both). Perfect for automating exploratory data analysis (EDA).

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
To install the development version from git, use:
```bash
$ pip install git+https://github.com/UBC-MDS/summarease.git
```

## Usage

```python
from summarease.summarize_dtypes import summarize_dtypes_table
from summarease.summarize_numeric import summarize_numeric, plot_numeric_density, plot_correlation_heatmap
from summarease.summarize_target import summarize_target_df, summarize_target_balance_plot
from summarease.summarize import summarize, validate_or_create_path, add_image, add_table, switch_page_if_needed

```

## Contributing

Interested in contributing? Check out the contributing guidelines. 

Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`summarease` is licensed under the terms of the MIT license.

## Contributors

`summarease` was created by Hrayr Muradyan, Yun Zhou, Stephanie Wu, and Zuer Zhong.

## Credits

`summarease` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
