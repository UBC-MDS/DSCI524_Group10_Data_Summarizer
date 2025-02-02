import pandas as pd
from fpdf import FPDF
from pathlib import Path
from summarease.summarize_numeric import summarize_numeric
from summarease.summarize_target import summarize_target_df, summarize_target_balance_plot
from summarease.summarize_dtypes import summarize_dtypes_table
from PIL import Image


def validate_or_create_path(path):
    """
    Validates if the provided path is a valid `Path` object. If the path represents a file, 
    it ensures the parent directory exists, creating it if necessary. If the path represents 
    a directory, it ensures the directory exists, creating it if necessary.

    Args:
        path (Path): The path to validate or create. Can represent a file or directory.

    Raises:
        TypeError: If the provided `path` is not an instance of `Path`.

    Notes:
        - If the path is a file and the parent directory does not exist, the function creates 
          the necessary parent directories.
        - If the path is a directory and it does not exist, the function creates it, including 
          any necessary parent directories.
        - The `mkdir` method is used with `parents=True` and `exist_ok=True`, which ensures 
          that parent directories are created if they do not exist, and no error is raised 
          if the path already exists.
    """
    if not isinstance(path, Path):
        raise TypeError(f"Expected a Path object, got {type(path)}.")
    
    # Check if the input is a file or not, if not, then check if the directory exists
    if not path.is_file():
        path.mkdir(parents=True, exist_ok=True)
            


def add_image(pdf, image_path, pdf_height, pdf_width, element_padding=15):
    """
    Adds an image to a PDF document at the current y-position with consideration for page size 
    and scaling. If the image height exceeds the remaining space on the current page, a new page 
    is added to the PDF. The image is scaled proportionally to fit the page width while maintaining 
    the aspect ratio.

    Args:
        pdf: A FPDF object representing the PDF document to which the image will be added.
        image_path (str or Path): The file path to the image to be added. It supports various image 
                                  formats such as .jpg, .jpeg, .png, .gif, .bmp, .tiff, and .webp.
        pdf_height (float): The total height of the PDF page in units consistent with the FPDF settings.
        pdf_width (float): The total width of the PDF page in units consistent with the FPDF settings.
        element_padding (int, optional): The padding (in units consistent with FPDF) to be applied between 
                                          the image and the page's top margin. Default is 15.

    Returns:
        pdf: The updated FPDF object with the image added at the correct position.

    Notes:
        - The function checks if the image file exists and has a valid image extension.
        - The image is scaled to fit within the page width, and if necessary, a new page is added.
        - The function assumes a DPI of 96 for the image size conversion from pixels to millimeters.
        - If the image height exceeds the remaining space on the current page, a new page is created before adding the image.
    """
    assert isinstance(pdf, FPDF), f"Argument 'pdf' should be FPDF class. You have {type(pdf)}."
    assert isinstance(image_path, Path) or isinstance(image_path, str), f"Argument 'image_path' should be a Path class or string. You have {type(image_path)}."
    assert isinstance(pdf_height, int) or isinstance(pdf_height, float), f"Argument 'pdf_height' should be an integer or float. You have {type(pdf_height)}."
    assert isinstance(pdf_width, int) or isinstance(pdf_height, float), f"Argument 'pdf_width' should be an integer or float. You have {type(pdf_width)}."
    assert isinstance(element_padding, int), f"Argument 'element_padding' should be an integer. You have {type(element_padding)}."

    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    image_path = Path(image_path)
    assert image_path.suffix in image_extensions, f"Unsupported image format. Should be {image_extensions}"
    image_path_str = str(image_path)
    y_position = pdf.get_y()  
    page_height = pdf_height - 2 * pdf.t_margin

    if not image_path.is_file():
        raise ValueError(f"File not found: {image_path_str}")

    if image_path.is_file():
        # Check if the file has a valid image extension
        if image_path.suffix.lower() in image_extensions:
            with Image.open(image_path_str) as img:
                _, image_height = img.size
                dpi = 96  
                element_height_mm = image_height / dpi * 25.4

                if element_height_mm > page_height:
                    scale_factor = page_height / element_height_mm
                else:
                    scale_factor = 1
    if y_position + element_height_mm > page_height:
        pdf.add_page()

    pdf.ln(pdf.get_y()) 
    y_position = pdf.get_y()
    # Add the image to the PDF
    pdf.image(image_path_str, x=pdf.l_margin, y=y_position + element_padding, w=int(scale_factor*(pdf_width - 2 * pdf.l_margin))) 
    pdf.ln(element_height_mm + element_padding) 

    # Manually update y_position after adding the image
    y_position = pdf.get_y()

    return pdf

def add_table(pdf, table, pdf_height, pdf_width, element_padding=15):
    """
    Adds a table to the PDF document with the provided data, scaling the column widths to fit 
    within the page width while maintaining their relative proportions. The first row (header) 
    has a gray background, and the first column (index) is highlighted with a gray background.

    Args:
        pdf: A FPDF object representing the PDF document to which the table will be added.
        table (pandas.DataFrame): The table containing the data to be added. The first column 
                                  (index) will be inserted as a new column in the table.
        pdf_height (float): The total height of the PDF page in units consistent with the FPDF settings.
        pdf_width (float): The total width of the PDF page in units consistent with the FPDF settings.
        element_padding (int, optional): The padding (in units consistent with FPDF) to be applied 
                                          around the table. Default is 15.

    Returns:
        pdf: The updated FPDF object with the table added.

    Notes:
        - The function calculates the maximum column width based on the longest entry or column name, 
          scaling the column widths to fit the available page width while maintaining relative proportions.
        - The first row (header) is filled with a light gray background, and the first column (index) 
          is also highlighted with a gray background for better readability.
        - Column names are truncated if they are too long to fit in the cell, and the font size is adjusted 
          accordingly for long column names.
        - Numeric values are rounded to 2 decimal places for consistency.
    """
    assert isinstance(pdf, FPDF), f"Argument 'pdf' should be FPDF class. You have {type(pdf)}."
    assert isinstance(table, pd.DataFrame), f"Argument 'table' should be a pandas Dataframe. You have {type(table)}."
    assert isinstance(pdf_height, int) or isinstance(pdf_height, float), f"Argument 'pdf_height' should be an integer or float. You have {type(pdf_height)}."
    assert isinstance(pdf_width, int) or isinstance(pdf_height, float), f"Argument 'pdf_width' should be an integer or float. You have {type(pdf_width)}."
    assert isinstance(element_padding, int), f"Argument 'element_padding' should be an integer. You have {type(element_padding)}."
    assert not table.empty, f"The table shouldn't be empty"

    pdf.set_font('Arial', '', 9)
    
    # Insert index as a new column (at the start)
    table.insert(0, 'Index', table.index)

    # Calculate maximum column width based on the longest entry
    col_widths = []
    for col in table.columns:
        max_length = max(table[col].apply(lambda x: len(str(x))).max(), len(col)) 
        col_widths.append(max_length * 2)  

    # Adjust the index column width to be smaller (as index is usually smaller)
    col_widths[0] = max(col_widths[0], 20)  

    total_width = sum(col_widths)
    
    # Scale column widths to fit within the page width, maintaining the relative proportions
    scale_factor = (pdf_width - 2 * element_padding) / total_width
    col_widths = [w * scale_factor for w in col_widths]

    # Set gray color for the first row and first column
    pdf.set_fill_color(230, 230, 230)  

    # Add table header with gray background for the first row
    for i, col in enumerate(table.columns):
        col_name = col
        # Convert col_widths[i] to integer for proper slicing
        max_length_for_col = int(col_widths[i] // 2)   
        # If the column name is longer than the cell, truncate or wrap the text
        if len(col_name) > max_length_for_col:  
            col_name = col_name[:max_length_for_col] + '...'  
            pdf.set_font('Arial', '', 8)  
        pdf.cell(col_widths[i], 10, col_name, border=1, align='C', fill=True)
        pdf.set_font('Arial', '', 9)  
    pdf.ln()

    # Add table rows with gray background for the first column (index)
    for i in range(len(table)):
        for j, col in enumerate(table.columns):
            value = table[col].iloc[i]
            # Round numeric values to 2 decimals
            if isinstance(value, (int, float)):
                value = round(value, 2)
            
            # Apply gray background for the first column (index)
            if j == 0:  
                pdf.set_fill_color(230, 230, 230)  
                pdf.cell(col_widths[j], 10, str(value), border=1, align='C', fill=True)
            else:
                pdf.cell(col_widths[j], 10, str(value), border=1, align='C', fill=False)
        pdf.ln()

    return pdf

def switch_page_if_needed(pdf):
    assert isinstance(pdf, FPDF), f"Argument 'pdf' should be FPDF class. You have {pdf}"
    if pdf.get_y() > 50:
        pdf.add_page()
    return pdf

def summarize(dataset: pd.DataFrame,
              dataset_name: str = "Dataset Summary", 
              description: str = "Dataset summary generated by summarease.", 
              show_observations: str = "random", 
              show_n_observations: int = 5,
              show_warnings: bool = True,
              summarize_by: str = "mix", 
              auto_cleaning: bool = False, 
              target_variable: str = None,
              target_type: str = "categorical",
              output_file: str = "summary.pdf",
              output_dir: str = "./summarease_summary/"
):
    """
    Summarizes the given dataset by generating various statistics, visualizations, 
    and/or tables based on the provided options.

    Parameters:
    -----------
    dataset : pd.DataFrame
        The dataframe to be summarized.

    dataset_name : str, optional, default="Dataset Summary"
        Represents the title of the summary, can be simply the name of the dataset.

    description : str, optional, default="Dataset summary generated by summarease."
        A description of the dataset to provide context in the summary.

    show_observations : str, optional, default="random"
        Specifies how to display sample observations from the dataset:
        - "random" : Displays random observations.
        - "head" : Displays the first few observations.
        - "tail" : Displays the last few observations.

    show_n_observations : int, optional, default=5
        The number of observations to show.

    show_warnings : bool, optional, default=True
        Whether to include the warnings in the summary report or not.

    summarize_by : str, optional, default="mix"
        Specifies what visual elements to use when summarizing the dataset:
        - "table" : Summarize using tables.
        - "plot" : Summarize using plots.
        - "mix" : Automatically choose a suitable summarization method (table or plot) for each part.

    auto_cleaning : bool, optional, default=False
        If True, automatically cleans the dataset by:
        - Converting column names to lowercase, removing spaces and symbols.
        - Replacing invalid values (e.g., "?", "NA", "-") with NaN.
        - Checking for incorrect data types and attempting to fix them.

    target_variable : str, optional, default=None
        The name of the target variable in the dataset. This helps in identifying the dependent variable for further analysis.

    target_type : str, within {"categorical", "numerical"}
        The type of target variable.

    output_file : str, optional, default="summary.pdf"
        The name of the output file where the summary will be saved.

    output_dir : str, optional, default="./summarease_summary/"
        The directory where the output summary file will be saved.

    Returns:
    --------
    None
        This function outputs the summary of the dataset in an output file, including statistical summaries, visualizations, and cleaning steps (if applicable).

    Notes:
    ------
    - The `show_observations` parameter can be customized to display a certain number of observations.
    - The `summarize_by` parameter offers flexibility in the type of summary (table, plot, or mix).
    - `auto_cleaning` does basic cleaning of the dataset before doing the summary.

    Example:
    --------
    >>> import pandas as pd
    >>> from summarease import summarize
    >>> data = pd.DataFrame({
    ...     "Age": [23, 45, 31, 35, 29],
    ...     "Gender": ["Male", "Female", "Female", "Male", "Male"],
    ...     "Salary": [50000, 60000, 75000, 80000, 65000]
    ... })
    >>> summarize(
    ...     dataset=data, 
    ...     dataset_name="Employee Data Summary", 
    ...     description="Summary of employee demographic and salary data.",
    ...     summarize_by="plot",
    ...     auto_cleaning=True,
    ...     output_file="employee_summary.pdf"
    ... )
    # This will generate a summary of the `data` dataframe, display the first three observations,
    # clean the dataset, and save the summary as 'employee_summary.pdf' in the default output directory.
    """
    assert isinstance(dataset, pd.DataFrame), f"Argument 'dataset' should be pandas dataframe (pd.DataFrame)! You have {type(dataset)}."
    assert isinstance(dataset_name, str), f"Argument 'dataset_name' should be string (str)! You have {type(dataset_name)}."
    assert isinstance(description, str), f"Argument 'description' should be string (str)! You have {type(description)}."
    assert isinstance(show_observations, str), f"Argument 'show_observations' should be a string (str)! You have {type(show_observations)}."
    assert isinstance(show_n_observations, int), f"Argument 'show_n_observations' should be an integer (int)! You have {type(show_n_observations)}."
    assert isinstance(show_warnings, bool), f"Argument 'show_warnings' should be a boolean (bool)! You have {type(show_warnings)}."
    assert isinstance(summarize_by, str), f"Argument 'summarize_by' should be a string (str)! You have {type(summarize_by)}."
    assert isinstance(auto_cleaning, bool), f"Argument 'auto_cleaning' should be a boolean (bool)! You have {type(auto_cleaning)}."
    if target_variable is not None:
        assert isinstance(target_variable, str), f"Argument 'target_variable' should be a string (str)! You have {type(target_variable)}."
        assert isinstance(target_type, str), f"Argument 'target_type' should be a string (str)! You have {type(target_type)}."
    assert isinstance(output_file, str), f"Argument 'output_file' should be a string (str)! You have {type(output_file)}."
    assert isinstance(output_dir, str), f"Argument 'output_dir' should be a string (str)! You have {type(output_dir)}."
    assert show_observations in {"random", "head", "tail"}, f"Argument 'show_observations' should be one of the following options: [random, head, tail]! You have {show_observations}."

    summarize_by = summarize_by.lower()
    assert summarize_by in {"table", "plot", "mix"}, f"Argument 'summarize_by' should be one of the following options: [table, plot, mix]! You have {summarize_by}."

    output_dir = Path(output_dir)
    output_path = output_dir / output_file

    assert (output_path.suffix == ".pdf") or (output_path.suffix == ""), f"The 'output_file' should either have a .pdf extension or no extension! You have {output_path.suffix}."

    # If the path doesn't exist, create it
    validate_or_create_path(output_dir)

    if summarize_by in {"plot", "mix"}:
        plot_output_path = output_dir / "img"
        validate_or_create_path(plot_output_path)


    dataset_shape = dataset.shape
    assert (dataset_shape[1] >= 2 and dataset_shape[1] <= 15), f"The function currently supports dataframes having less than 15 columns and more than 2 columns! You have {dataset_shape[1]}"

    # Create the PDF
    pdf = FPDF()

    # Add a new page
    pdf.add_page()

    page_width = pdf.w
    page_height = pdf.h

    element_padding = 10
    text_line_padding = 10

    # Set the font to Helvetica, set the size, write the title
    pdf.set_font("Helvetica", size=15)
    pdf.cell(page_width - 2 * pdf.l_margin, element_padding, txt=dataset_name, ln=True, align='C')

    # Change the size for the description and write it
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(page_width - 2 * pdf.l_margin, text_line_padding, txt=description, align='L')

    pdf = switch_page_if_needed(pdf)
    pdf.set_font("Helvetica", size=13)
    pdf.cell(page_width - 2 * pdf.l_margin, element_padding, txt="Numeric Columns Summary", ln=True, align='C')

    if summarize_by == "plot":
        summarized_numeric_output = summarize_numeric(dataset, summarize_by="plot")
        if summarized_numeric_output:
            for key, item in summarized_numeric_output.items():
                plot_file = plot_output_path / f'{key}.png'
                str_plot_file = str(plot_file)
                item.save(plot_file)
                pdf = add_image(pdf, image_path=str_plot_file, pdf_height=page_height, pdf_width=page_width, element_padding=10)

        if target_variable is not None:
            pdf = switch_page_if_needed(pdf)
            pdf.set_font("Helvetica", size=13)
            pdf.cell(page_width - 2 * pdf.l_margin, element_padding, txt="Target Variable Summary", ln=True, align='C')
            pdf.set_font("Helvetica", size=11)
            pdf.multi_cell(page_width - 2 * pdf.l_margin, text_line_padding, txt=f"Target variable is a {target_type} variable. Please find the information about the target variable below:", align='L')
            summarized_target_output = summarize_target_df(dataset, target_variable, target_type)
            summarized_target_plot = summarize_target_balance_plot(summarized_target_output)
            target_plot_file = plot_output_path / "target_plot.png"
            summarized_target_plot.save(target_plot_file)
            pdf = add_image(pdf, target_plot_file, pdf_height=page_height, pdf_width=page_width, element_padding=0)

    elif summarize_by == "table":
        summarized_numeric_output = summarize_numeric(dataset, summarize_by="table")
        if summarized_numeric_output:
            pdf = add_table(pdf, table = summarized_numeric_output["numeric_describe"], pdf_height=page_height, pdf_width=page_width, element_padding=15)

        if target_variable is not None:
            pdf = switch_page_if_needed(pdf)
            summarized_target_output = summarize_target_df(dataset, target_variable, target_type)
            pdf.set_font("Helvetica", size=13)
            pdf.cell(page_width - 2 * pdf.l_margin, element_padding, txt="Target Variable Summary", ln=True, align='C')
            pdf.set_font("Helvetica", size=11)
            pdf.multi_cell(page_width - 2 * pdf.l_margin, text_line_padding, txt=f"Target variable is a {target_type} variable. Please find the information about the target variable below:", align='L')
            pdf = add_table(pdf, table = summarized_target_output, pdf_height=page_height, pdf_width=page_width, element_padding=15)

    summarized_dtypes_table = summarize_dtypes_table(dataset)
    pdf.set_font("Helvetica", size=13)
    pdf.cell(page_width - 2 * pdf.l_margin, element_padding, txt="Dataset Data Types Summary", ln=True, align='C')
    pdf = add_table(pdf, table = summarized_dtypes_table, pdf_height=page_height, pdf_width=page_width, element_padding=15)

    pdf.output(output_path)
    assert output_path.exists(), "Something went wrong... The PDF output was not saved."
    print("PDF created!")

