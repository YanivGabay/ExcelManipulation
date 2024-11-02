import pandas as pd
from tkinter import messagebox
from constants import EXCEL_COLUMN_MAPPING
import tkinter as tk
from constants import RULES_COLUMN_MAPPING




def standardize_vehicle_number(vehicle_number, length=8):
    """Standardize the vehicle number to ensure it has the correct number of digits."""
    return str(vehicle_number).zfill(length)

def update_excel_row(df, row_index, record, rules_df, rules_list):
    """Update Excel row with data from the record based on a mapping."""
    updates_made = 0
    for field, excel_col_index in EXCEL_COLUMN_MAPPING.items():
        if field in record:
            value_to_insert = str(record[field]).strip()  # Convert to string and strip whitespace
            if df.iat[row_index, excel_col_index] != value_to_insert:  # Check if the update is necessary
                df.iat[row_index, excel_col_index] = value_to_insert
                updates_made += 1
    if updates_made > 0:
        # Check if the value in column 'P' matches any value in the rules_list
        value_in_p_column = df.iat[row_index, df.columns.get_loc("P")]
        if value_in_p_column in rules_list:
            # Find the index of the matching value in the rules_list
            rules_row_index = rules_list.index(value_in_p_column)
            
            # Update the row with values from the rules_df based on RULES_COLUMN_MAPPING
            for original_column, rules_col_value in RULES_COLUMN_MAPPING.items():
                df.iat[row_index, df.columns.get_loc(original_column)] = rules_df.iat[rules_row_index, rules_col_value]
    return updates_made

def transfer_data_to_excel(file_path, text_data, output_text, rules_df, rules_list):
    try:
        df = pd.read_excel(file_path, dtype=str)
        vehicle_number_col_index = 10  # Adjust as needed for the correct column index for vehicle numbers
        ### GAL SAID THIS IS OUR "KEY"
        df['standardized_vehicle_number'] = df.iloc[:, vehicle_number_col_index].apply(standardize_vehicle_number)
        
        total_rows = 0
        rows_updated = 0
        unmatched_vehicles = []

        # Iterate over each record
        for record in text_data:
            vehicle_number_from_record = record.get('vehicle_number', '').strip()
            row_indices = df.index[df['standardized_vehicle_number'] == vehicle_number_from_record].tolist()
            total_rows += 1

            if row_indices:
                for row_index in row_indices:
                    if update_excel_row(df, row_index, record,rules_df,rules_list) > 0:
                        rows_updated += 1
                        
            else:
                unmatched_vehicles.append(vehicle_number_from_record)

        # Saving changes if any rows were updated
        if rows_updated > 0:

            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
                
            output_text.insert(tk.END, f"Excel file updated: {rows_updated} rows modified out of {total_rows} processed.\n")
        else:
            output_text.insert(tk.END, "No rows modified.\n")

        # Report unmatched vehicle numbers
        if unmatched_vehicles:
            output_text.insert(tk.END, f"Unmatched vehicles ({len(unmatched_vehicles)}): {', '.join(unmatched_vehicles)}\n")
        else:
            output_text.insert(tk.END, "All vehicle numbers matched successfully.\n")

    except Exception as e:
        messagebox.showerror("Excel Error", f"Failed to update Excel file: {str(e)}")
        print(f"Exception occurred: {e}")
