import pandas as pd

def read_xlsm_file(file_path):
    # Read the Excel file
    try:
        # Assuming the file has only one sheet, or we're interested in the first sheet
        df = pd.read_excel(file_path, engine='openpyxl')
        return df
    except Exception as e:
        print(f"Error occurred: {e}")
        return None