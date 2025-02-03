import pytest
import os
from pathlib import Path
from unittest.mock import patch
import pandas as pd
import shutil
from fpdf import FPDF
from summarease.summarize import summarize, validate_or_create_path, add_image, add_table, switch_page_if_needed
from unittest.mock import MagicMock
import time

# ---------------------------------------------
# tests for summarize

@pytest.fixture
def mock_dataset():
    # A sample dataset for testing
    return pd.DataFrame({
        "Age": [23, 45, 31, 35, 29],
        "Gender": ["Male", "Female", "Female", "Male", "Male"],
        "Salary": [50000, 60000, 75000, 80000, 65000]
    })


@pytest.fixture
def cleanup_files():
    # This fixture ensures cleanup of files and directories after each test
    yield
    
    # Define the directories to clean up
    dirs_to_cleanup = [
        Path("./summarease_summary_test/"),
        Path("./summarease_summary/")
    ]
    
    for output_dir in dirs_to_cleanup:
        if output_dir.exists() and output_dir.is_dir():
            # Recursively remove all files in the directory
            for file in output_dir.rglob('*'): 
                try:
                    file.unlink()  
                except PermissionError:
                    print(f"Permission error while deleting {file}")
                    continue
            try:
                output_dir.rmdir()  
            except OSError:
                shutil.rmtree(output_dir)
                time.sleep(0.1)  

def test_create_images():
    # Define the image paths and their respective sizes
    image_details = [
        ("large_image.jpg", 2000, 3000),  
        ("small_image.jpg", 200, 300),   
        ("normal_image.jpg", 800, 600)    
    ]

    # Create and save each image
    for image_path, width, height in image_details:
        image = Image.new("RGB", (width, height), color=(255, 255, 255))  
        image.save(image_path)

def test_invalid_dataset_type(mock_dataset):
    with pytest.raises(AssertionError, match="Argument 'dataset' should be pandas dataframe"):
        summarize(dataset="not_a_dataframe")


def test_invalid_show_observations(mock_dataset):
    with pytest.raises(AssertionError, match="Argument 'show_observations' should be one of the following options:"):
        summarize(dataset=mock_dataset, show_observations="invalid_option")


def test_invalid_summarize_by(mock_dataset):
    with pytest.raises(AssertionError, match="Argument 'summarize_by' should be one of the following options:"):
        summarize(dataset=mock_dataset, summarize_by="invalid_option")


def test_auto_cleaning_argument(mock_dataset):
    # Test when auto_cleaning is set to True, though here it's not fully implemented
    result = summarize(dataset=mock_dataset, auto_cleaning=True)
    # Assert that no errors occur with auto_cleaning set to True
    assert result is None


def test_output_directory_creation(mock_dataset, cleanup_files):
    # Set a custom output directory and file name
    output_file = "test_output.pdf"
    output_dir = "./summarease_summary_test/"

    # Run the function
    summarize(
        dataset=mock_dataset,
        output_file=output_file,
        output_dir=output_dir
    )

    output_path = Path(output_dir) / output_file

    # Check if the directory was created
    assert output_path.parent.exists()

    # Check if the PDF file has the correct name
    assert output_path.name == output_file


def test_file_extension_validation(mock_dataset):
    with pytest.raises(AssertionError, match="The 'output_file' should either have a .pdf extension or no extension"):
        summarize(dataset=mock_dataset, output_file="invalid_extension.txt")


def test_valid_summarize_call(mock_dataset, cleanup_files):
    # Valid call to summarize
    summarize(
        dataset=mock_dataset,
        dataset_name="Test Dataset",
        description="This is a test dataset.",
        target_variable = "Gender",
        summarize_by="table",
        auto_cleaning=True,
        output_file="test_summary.pdf",
        output_dir="./summarease_summary_test/"
    )

    # Check if the output directory and file were created
    output_path = Path("./summarease_summary_test/test_summary.pdf")
    assert output_path.exists()


def test_invalid_target_variable(mock_dataset):
    with pytest.raises(AssertionError, match="Argument 'target_variable' should be a string"):
        summarize(dataset=mock_dataset, target_variable=123)


# Check if the plot is created after the numeric analysis
def test_check_if_image_is_saved(mock_dataset):
    output_dir = "./summarease_summary_test/"
    output_dir_path = Path(output_dir)
    summarize(
        dataset=mock_dataset,
        dataset_name="Test Dataset",
        description="This is a test dataset.",
        target_variable = "Gender",
        summarize_by="plot",
        auto_cleaning=True,
        output_file="test_summary.pdf",
        output_dir=output_dir
    )

    assert (output_dir_path / "img" / "numeric_plot.png").exists()
    assert (output_dir_path / "img" / "corr_plot.png").exists()



# --------------------------------------------------------------------------------------------------------------------------------------------------

# Tests for add_table

def test_add_table_normal():
    pdf = FPDF()
    pdf.add_page()
    data = {
        "Name": ["Alice", "Bob"],
        "Age": [25, 30]
    }
    table = pd.DataFrame(data)
    result_pdf = add_table(pdf, table, 297, 210)
    assert result_pdf is not None

def test_add_table_various_data_types():
    pdf = FPDF()
    pdf.add_page()
    data = {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "Score": [85.5, 90.2, 95.3],
        "Passed": [True, False, True]
    }
    table = pd.DataFrame(data)
    result_pdf = add_table(pdf, table, 297, 210)
    assert result_pdf is not None

def test_add_table_single_column():
    pdf = FPDF()
    pdf.add_page()
    data = {
        "Name": ["Alice", "Bob", "Charlie"]
    }
    table = pd.DataFrame(data)
    result_pdf = add_table(pdf, table, 297, 210)
    assert result_pdf is not None

if __name__ == '__main__':
    pytest.main()


def test_data_with_long_column_names():
    pdf = FPDF()
    pdf.add_page()
    data = {
        "very_long_column_name_that_should_be_truncated": list(range(0, 30)),
        "very_long_column_name_that_should_be_truncated1": list(range(0, 30)),
        "very_long_column_name_that_should_be_truncated2": list(range(0, 30)),
        "very_long_column_name_that_should_be_truncated3": list(range(0, 30)),
    }
    table = pd.DataFrame(data)
    result_pdf = add_table(pdf, table, 297, 210)
    assert result_pdf is not None

# --------------------------------------------------------------------------------------------------------------------------------------------------

# Tests for add_image


import pytest
from unittest.mock import patch
from pathlib import Path
from fpdf import FPDF
from PIL import Image

def mock_image_open(image_path):
    class MockImage:
        def __init__(self, width, height):
            self.size = (width, height)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            pass

    # Simulate different image sizes based on file names
    if "large" in Path(image_path).name:
        return MockImage(2000, 3000)  
    elif "small" in Path(image_path).name:
        return MockImage(200, 300)    
    else:
        return MockImage(800, 600)   


# Test for adding large image
@patch("PIL.Image.open", side_effect=mock_image_open)
@patch("os.path.exists", return_value=True)
@patch("pathlib.Path.is_file", return_value=True)  
def test_add_image_large(mock_isfile, mock_exists, mock_open):
    pdf = FPDF()
    pdf.add_page()
    image_path = Path("large_image.jpg")
    pdf_height = 297
    pdf_width = 210
    element_padding = 15

    pdf = add_image(pdf, image_path, pdf_height, pdf_width, element_padding)
    assert pdf is not None

# Similarly update other tests:
@patch("PIL.Image.open", side_effect=mock_image_open)
@patch("os.path.exists", return_value=True)
@patch("pathlib.Path.is_file", return_value=True)  
def test_add_image_small(mock_isfile, mock_exists, mock_open):
    pdf = FPDF()
    pdf.add_page()
    image_path = Path("small_image.jpg")
    pdf_height = 297
    pdf_width = 210
    element_padding = 15

    pdf = add_image(pdf, image_path, pdf_height, pdf_width, element_padding)
    assert pdf is not None

@patch("PIL.Image.open", side_effect=mock_image_open)
@patch("os.path.exists", return_value=True)
@patch("pathlib.Path.is_file", return_value=True)  
def test_add_image_normal(mock_isfile, mock_exists, mock_open):
    pdf = FPDF()
    pdf.add_page()
    image_path = Path("normal_image.jpg")
    pdf_height = 297
    pdf_width = 210
    element_padding = 15

    pdf = add_image(pdf, image_path, pdf_height, pdf_width, element_padding)
    assert pdf is not None

# Test for invalid PDF height type
def test_invalid_pdf_height_type():
    pdf = FPDF()
    pdf.add_page()
    image_path = Path("valid_image.jpg")
    pdf_height = "invalid_height"  
    pdf_width = 210
    element_padding = 15

    with pytest.raises(AssertionError, match="Argument 'pdf_height' should be an integer or float. You have"):
        add_image(pdf, image_path, pdf_height, pdf_width, element_padding)

# Test for invalid PDF width type
def test_invalid_pdf_width_type():
    pdf = FPDF()
    pdf.add_page()
    image_path = Path("valid_image.jpg")
    pdf_height = 297
    pdf_width = "invalid_width"  
    element_padding = 15

    with pytest.raises(AssertionError, match="Argument 'pdf_width' should be an integer or float. You have"):
        add_image(pdf, image_path, pdf_height, pdf_width, element_padding)

# Test for invalid image path type
def test_invalid_image_path_type():
    pdf = FPDF()
    pdf.add_page()
    image_path = 12345  
    pdf_height = 297
    pdf_width = 210
    element_padding = 15

    with pytest.raises(AssertionError, match="Argument 'image_path' should be a Path class or string. You have"):
        add_image(pdf, image_path, pdf_height, pdf_width, element_padding)

# Test for invalid PDF type
def test_invalid_pdf_type():
    pdf = "not_a_pdf_object"  
    image_path = Path("valid_image.jpg")
    pdf_height = 297
    pdf_width = 210
    element_padding = 15

    with pytest.raises(AssertionError, match="Argument 'pdf' should be FPDF class. You have"):
        add_image(pdf, image_path, pdf_height, pdf_width, element_padding)

# Test for invalid element padding argument
def test_invalid_element_padding():
    pdf = FPDF()
    image_path = Path("valid_image.jpg")
    pdf_height = 297
    pdf_width = 210
    element_padding = 15.34

    with pytest.raises(AssertionError, match="Argument 'element_padding' should be an integer. You have"):
        add_image(pdf, image_path, pdf_height, pdf_width, element_padding)

# Test for invalid element padding argument
def test_invalid_image_extension():
    pdf = FPDF()
    image_path = Path("valid_image.csv")
    pdf_height = 297
    pdf_width = 210
    element_padding = 15

    with pytest.raises(AssertionError, match="Unsupported image format. Should be"):
        add_image(pdf, image_path, pdf_height, pdf_width, element_padding)

# Test for cleaning images (checking if files exist before deletion)
def test_clean_images():
    small_image = Path("small_image.jpg")
    normal_image = Path("normal_image.jpg")
    large_image = Path("large_image.jpg")

    for image_path in [small_image, normal_image, large_image]:
        if image_path.exists():
            image_path.unlink()

# image doesn't exist
def test_image_not_found():
    pdf = FPDF()
    pdf.add_page()
    image_path = Path("valid_image.jpg")
    pdf_height = 297
    pdf_width = 210
    element_padding = 15

    with pytest.raises(ValueError, match="File not found: "):
        add_image(pdf, image_path, pdf_height, pdf_width, element_padding)
        
# --------------------------------------------------------------------------------------------------------------------------------------------------
# Tests for validate_or_create_path


def test_create_parent_directory():
    test_path = Path("/tmp/non_existent_directory/test.txt")
    
    # Ensure the parent directory does not exist
    assert not test_path.parent.exists()
    
    # Run the function
    validate_or_create_path(test_path)
    
    # Check if the parent directory is created
    assert test_path.parent.exists()
    
    # Clean up after test
    shutil.rmtree(test_path.parent, ignore_errors=True)

def test_parent_directory_exists():
    test_path = Path("/tmp/existing_directory/test.txt")
    
    # Create the parent directory before testing
    os.makedirs(test_path.parent, exist_ok=True)
    
    # Run the function (it should not alter anything)
    validate_or_create_path(test_path)
    
    # Check if the parent directory exists (no change should occur)
    assert test_path.parent.exists()
    
    # Clean up after test
    shutil.rmtree(test_path.parent)

def test_existing_file_path():
    test_path = Path("/tmp/existing_directory/test.txt")
    
    # Create the parent directory and a file
    os.makedirs(test_path.parent, exist_ok=True)
    test_path.touch()
    
    # Run the function (it should not alter anything)
    validate_or_create_path(test_path)
    
    # Check that the parent directory exists
    assert test_path.parent.exists()
    
    # Clean up after test
    test_path.unlink()
    shutil.rmtree(test_path.parent)

def test_existing_directory():
    test_path = Path("/tmp/existing_directory")
    
    # Create the directory if it doesn't exist
    os.makedirs(test_path, exist_ok=True)
    
    # Run the function (it should not alter anything)
    validate_or_create_path(test_path)
    
    # Ensure the directory exists
    assert test_path.exists()
    
    # Clean up after test
    shutil.rmtree(test_path)

def test_relative_path():
    test_path = Path("relative_dir/test.txt")
    
    # Ensure the parent directory does not exist
    assert not test_path.parent.exists()
    
    # Run the function
    validate_or_create_path(test_path)
    
    # Check if the parent directory is created
    assert test_path.parent.exists()
    
    # Clean up after test
    shutil.rmtree(test_path.parent)

def test_root_level_path():
    test_path = Path("/tmp/test.txt")  
    
    # Run the function
    validate_or_create_path(test_path)
    
    # Ensure that the function did not attempt to create anything above root
    assert test_path.parent == Path("/tmp")
    
    # Check that the parent directory exists
    assert test_path.parent.exists()

def test_invalid_path():
    # Test when path is not a Path object
    try:
        validate_or_create_path("not_a_path")  
        assert False, "Expected TypeError for non-Path object"
    except TypeError:
        pass


def test_no_page_added_if_get_y_below_threshold():
    # Create a mock FPDF instance
    pdf = MagicMock(spec=FPDF)
    pdf.get_y.return_value = 40  # Y-coordinate is less than 50, so no page should be added

    result = switch_page_if_needed(pdf)

    # Ensure add_page was not called
    pdf.add_page.assert_not_called()
    assert result is pdf  # Ensure pdf is returned unchanged

def test_page_added_if_get_y_above_threshold():
    # Create a mock FPDF instance
    pdf = MagicMock(spec=FPDF)
    pdf.get_y.return_value = 60  # Y-coordinate is greater than 50, so a page should be added

    result = switch_page_if_needed(pdf)

    # Ensure add_page was called once
    pdf.add_page.assert_called_once()
    assert result is pdf  # Ensure pdf is returned unchanged

def test_invalid_pdf_argument():
    with pytest.raises(AssertionError):
        switch_page_if_needed("not_a_pdf_object")

    with pytest.raises(AssertionError):
        switch_page_if_needed(None)