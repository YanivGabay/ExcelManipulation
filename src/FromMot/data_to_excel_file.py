import pandas as pd
from tkinter import messagebox
from constants import EXCEL_COLUMN_MAPPING
import tkinter as tk



def transfer_data_to_excel(file_path, text_data, output_text):
    try:
        # Load the Excel file, ensuring all data is treated as string to prevent type mismatches
        df = pd.read_excel(file_path, dtype=str)

        df.iloc[:, 10] = df.iloc[:, 10].astype(str)

        updates_made = 0  # To track if any updates have been made

        # Iterate over each record
        for record in text_data:
            vehicle_number_from_record = str(record.get('vehicle_number')).strip()  # Ensure it's string and trimmed
            print(f"Processing record with vehicle number: {vehicle_number_from_record}")

            # Find row indices where the vehicle number matches
            row_indices = df.index[df.iloc[:, 10] == vehicle_number_from_record].tolist()

            if row_indices:
                print(f"Found matching vehicle number at indices: {row_indices}")
                for row_index in row_indices:
                    # Update columns based on the mapping and the record's data
                    for field, excel_col_index in EXCEL_COLUMN_MAPPING.items():
                        if field in record:
                            value_to_insert = str(record[field]).strip()  # Convert to string and strip whitespace
                            print(f"Attempting to update '{field}' with value '{value_to_insert}' at row {row_index}, col {excel_col_index}")
                            df.iat[row_index, excel_col_index] = value_to_insert
                            updates_made += 1
                            print(f"Updated '{field}' at row {row_index}, col {excel_col_index} with '{value_to_insert}'")
            else:
                print(f"No matching vehicle number found for: {vehicle_number_from_record}")

        if updates_made:
            # Save the modified DataFrame back to the Excel file
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            output_text.insert(tk.END, f"Excel file updated successfully with {updates_made} updates.\n")
        else:
            output_text.insert(tk.END, "No updates made to the Excel file.\n")

    except Exception as e:
        messagebox.showerror("Excel Error", f"Failed to update Excel file: {str(e)}")
        print(f"Exception occurred: {e}")
'''
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
            if vehicle_number_from_record in df.iloc[:, 10].values:
                row_index = df.index[df.iloc[:, 10] == vehicle_number_from_record].tolist()
                if row_index:
                    row_index = row_index[0]  # Get the first matching index if there are multiple
                    print(f"Found matching vehicle number: {vehicle_number_from_record} at row {row_index}")
                    # Update columns based on the mapping and the record's data
                    for field, excel_col_index in EXCEL_COLUMN_MAPPING.items():
                        if field in record:
                            print(f"Updating field: {field} with value: {record[field]}")
                            df.at[row_index, df.columns[excel_col_index]] = record[field]

            # Save the modified DataFrame back to the Excel file
            with pd.ExcelWriter(xlsx_file_path) as writer:
                    df.to_excel(writer,index=False)
       
            output_text.insert(tk.END, "Excel file updated successfully based on vehicle numbers.\n")
  
    except Exception as e:
        messagebox.showerror("Excel Error", f"Failed to update Excel file: {str(e)}")
'''