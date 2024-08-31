import tkinter as tk
from tkinter import filedialog, messagebox
import os
import zipfile
from PIL import Image
import pandas as pd

def process_zip_files(folder_path,excel_path,output_field):
        """Processes all ZIP files in the selected folder."""
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".zip"):
                    zip_path = os.path.join(root, file)
                    extract_path = os.path.join(root, os.path.splitext(file)[0])
                    extract_zip_files(zip_path, extract_path)
                    clean_and_process_files(extract_path, os.path.splitext(file)[0],excel_path)


def extract_zip_files(zip_path, extract_path):
    """Extracts a zip file to the specified path."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
        print(f"Extracted ZIP: {zip_path}")

def clean_and_process_files(extract_path, zip_file_name, excel_file_path):
    """Processes files in the extracted directory and updates the Excel file."""
    # Load the Excel file
    df = pd.read_excel(excel_file_path, dtype=str)
    
    # Column indices
    id_of_report = 0  # Assuming 'A' column מפתח זיהוי
    update_col_index = 27     # Assuming 'AB' column is תמונת רגע התאונה

    has_updated = False

    for root, _, files in os.walk(extract_path):
        for file in files:
            if file in ['קישור לסרטון העבירה.jpg', 'מספר לוחית רישוי.jpg']:
                os.remove(os.path.join(root, file))
                print(f"Deleted: {os.path.join(root, file)}")
            if file == 'רגע העבירה.jpg':
                img_path = os.path.join(root, file)
                img = Image.open(img_path)
                new_file_name = f"{zip_file_name}_moment.png"
                new_file_path = os.path.join(root, new_file_name)
                img.save(new_file_path, 'PNG')
                os.remove(img_path)
                print(f"Converted and renamed: {new_file_path}")

                # Update the Excel file with the new file name where the vehicle number matches the zip file name
                row_indices = df.index[df.iloc[:, id_of_report] == zip_file_name].tolist()
                for row_index in row_indices:
                    df.iat[row_index, update_col_index] = new_file_name
                    has_updated = True
                    print(f"Updated Excel row {row_index} with new file name {new_file_name}")

    # Save the Excel file if there were updates
    if has_updated:
        with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
        print("Excel file updated successfully.")