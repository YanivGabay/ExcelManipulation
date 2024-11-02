import pandas as pd
from tkinter import messagebox
from constants import EXCEL_COLUMN_MAPPING
import tkinter as tk
from constants import RULES_COLUMN_MAPPING




def standardize_vehicle_number(vehicle_number, length=8):
    """Standardize the vehicle number to ensure it has the correct number of digits."""
    return str(vehicle_number).zfill(length)

def update_excel_row(df, row_index, record):
    """Update Excel row with data from the record based on a mapping."""
    updates_made = 0
    for field, excel_col_index in EXCEL_COLUMN_MAPPING.items():
        if field in record:
            value_to_insert = str(record[field]).strip()  # Convert to string and strip whitespace
            if df.iat[row_index, excel_col_index] != value_to_insert:  # Check if the update is necessary
                df.iat[row_index, excel_col_index] = value_to_insert
                updates_made += 1
    if updates_made > 0:
        rules_row_index = df.index[df['B'] == df.iat[row_index, 'P']].tolist()
        for original_column, rules_col_value in RULES_COLUMN_MAPPING.items():
            df.iat[row_index, original_column] = df.iat[rules_row_index, rules_col_value]

        
    return updates_made

def transfer_data_to_excel(file_path, text_data, output_text, rules_df):
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
                    if update_excel_row(df, row_index, record) > 0:
                        rows_updated += 1
                        add_rules_to_excel(df, row_index, record, rules_df)
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
def add_rules_to_excel(df, row_index, record, rules_df):

    value_in_p = df.at[row_index,'P']
    matched_rule = rules_df[rules_df[rules_df['B']] == value_in_p]

    if not matched_rule.empty:
        rule_row = matched_rule.iloc[0]
        df.at[row_index,'V'] = rule_row['H']
        # W and I
        df.at[row_index,'W'] = rule_row['I']
        #X and F
        df.at[row_index,'X'] = rule_row['F']
        # Y and G
        df.at[row_index,'Y'] = rule_row['G']

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