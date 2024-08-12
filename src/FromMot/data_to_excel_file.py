import pandas as pd
from tkinter import messagebox
from constants import EXCEL_COLUMN_MAPPING, VEHICLE_NUMBER_COLUMN_INDEX
import tkinter as tk

def transfter_data_to_excel(file_path, text_data, output_text):
    try:
        # Load the Excel file
        df = pd.read_excel(file_path)
        xlsx_file_path = file_path.replace('.xls', '.xlsx')
        
        # Ensure the DataFrame is updated to the new file
        df.to_excel(xlsx_file_path, index=False)
        
        # Iterate over each record
        for record in text_data:
            vehicle_number_from_record = record.get('vehicle_number')  # Get the vehicle number from the record
            print(f"Processing record with vehicle number: {vehicle_number_from_record}")
            
            # Find the row index where the vehicle number column matches the vehicle number from the record
            if vehicle_number_from_record in df.iloc[:, VEHICLE_NUMBER_COLUMN_INDEX].values:
                row_index = df.index[df.iloc[:, VEHICLE_NUMBER_COLUMN_INDEX] == vehicle_number_from_record].tolist()
                if row_index:
                    row_index = row_index[0]  # Get the first matching index if there are multiple
                    print(f"Found matching vehicle number: {vehicle_number_from_record} at row {row_index}")
                    # Update columns based on the mapping and the record's data
                    for field, excel_col_index in EXCEL_COLUMN_MAPPING.items():
                        if field in record:
                            print(f"Updating field: {field} with value: {record[field]}")
                            df.at[row_index, df.columns[excel_col_index]] = record[field]

            # Save the modified DataFrame back to the Excel file
            with pd.ExcelWriter(xlsx_file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
       
            output_text.insert(tk.END, "Excel file updated successfully based on vehicle numbers.\n")
  
    except Exception as e:
        messagebox.showerror("Excel Error", f"Failed to update Excel file: {str(e)}")
