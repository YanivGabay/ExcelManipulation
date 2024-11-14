import os
import zipfile
from PIL import Image
import pandas as pd
from typing import Any, Dict, List


def process_zip_files(folder_path: str, full_df: pd.DataFrame, output_folder: str) -> pd.DataFrame:
 
    if full_df is None:
        raise ValueError("The DataFrame 'full_df' cannot be None.")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")
    df = full_df.copy()
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".zip"):
                zip_path = os.path.join(root, file)
                zip_name = os.path.splitext(file)[0]
                extract_path = os.path.join(output_folder, zip_name)

                try:
                    extract_zip_files(zip_path, extract_path)
                    df = clean_and_process_files(extract_path, zip_name, df)
                except Exception as e:
                    error_message = f"Failed to process '{zip_path}': {str(e)}"
                    print(error_message)
                    raise RuntimeError(error_message) from e
    return df

def extract_zip_files(zip_path: str, extract_path: str) -> None:
 
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        print(f"Extracted ZIP: {zip_path} to {extract_path}")
    except zipfile.BadZipFile:
        raise zipfile.BadZipFile(f"The file '{zip_path}' is not a valid ZIP file or is corrupted.")
    except FileNotFoundError:
        raise FileNotFoundError(f"The ZIP file '{zip_path}' was not found.")
    except PermissionError:
        raise PermissionError(f"Permission denied while extracting '{zip_path}' to '{extract_path}'.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while extracting '{zip_path}': {str(e)}")

def convert_rename_image(root,file_path,zip_file_name,suffix):
                    img = Image.open(file_path)
                    new_file_name = f"{zip_file_name}_{suffix}.png"
                    new_file_path = os.path.join(root, new_file_name)
                    img.save(new_file_path, 'PNG')
                    img.close()
                    os.remove(file_path)
                    print(f"Converted and renamed: {new_file_path}")
                    return new_file_name

def clean_and_process_files(extract_path: str, zip_file_name: str, full_df: pd.DataFrame) -> pd.DataFrame:
 
    df = full_df.copy()
    # Column indices (0-based)
    id_of_report = 0       # Assuming column 'A' (index 0) is מפתח זיהוי (ID of report)
    update_col_index = 27  # Assuming column 'AB' (index 27) is תמונת רגע התאונה (Accident moment image)

    has_updated = False

    for root, _, files in os.walk(extract_path):
        for file in files:
            file_path = os.path.join(root, file)
            new_file_name : str = ""
            if file in ['מספר לוחית רישוי.jpg']:
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete '{file_path}': {str(e)}")

            if file == 'רגע העבירה.jpg':
                try:
                    new_file_name = convert_rename_image(root,file_path,zip_file_name,'accident_moment')
                    # Update the Excel file with the new file name where the vehicle number matches the ZIP file name
                    row_indices = df.index[df.iloc[:, id_of_report] == zip_file_name].tolist()
                    for row_index in row_indices:
                        df.iat[row_index, update_col_index] = new_file_name
                        has_updated = True
                        print(f"Updated Excel row {row_index} with new file name '{new_file_name}'")
                except Exception as e:
                    print(f"Failed to process image '{file_path}': {str(e)}")

            if file == 'קישור לסרטון העבירה.jpg':
                try:
                    new_file_name = convert_rename_image(root,file_path,zip_file_name,'accident_link')

                    # Update the Excel file with the new file name where the vehicle number matches the ZIP file name
                    row_indices = df.index[df.iloc[:, id_of_report] == zip_file_name].tolist()
                    for row_index in row_indices:
                        df.iat[row_index, update_col_index+1] = new_file_name
                        has_updated = True
                        print(f"Updated Excel row {row_index} with new file name '{new_file_name}'")
                except Exception as e:
                    print(f"Failed to process image '{file_path}': {str(e)}")


    return df
