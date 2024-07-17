import pandas as pd
from tkinter import messagebox
from constants import EXCEL_COLUMN_MAPPING
import tkinter as tk

def transfter_data_to_excel(file_path,text_data,output_text):
    try:
        # Load the Excel file
        df = pd.read_excel(file_path)

        # Iterate over each record
        for record in text_data:
            address_from_record = record.get('address')  # Get the address from the record
            # Find the row index where the first column matches the address from the record
            row_index = df[df.iloc[:, 0] == address_from_record].index
            if not row_index.empty:
                row_index = row_index[0]  # Get the first matching index
                # Update columns based on the mapping and the record's data
                for field, excel_col_index in EXCEL_COLUMN_MAPPING.items():
                    if field in record:
                        df.iat[row_index, excel_col_index] = record[field]

        # Save the modified DataFrame back to the Excel file
        with pd.ExcelWriter(file_path) as writer:
            df.to_excel(writer,engine = 'xlwt' ,index=False)
       
        output_text.insert(tk.END, "Excel file updated successfully based on addresses.\n")
  
    except Exception as e:
        messagebox.showerror("Excel Error", f"Failed to update Excel file: {str(e)}")