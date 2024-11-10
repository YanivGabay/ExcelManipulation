import datetime
import pandas as pd
from tkinter import messagebox
from typing import Any, Dict, List, Tuple
from src.FromMot.text_processing import reverse_word_if_hebrew
from constants import EXCEL_COLUMN_MAPPING, RULES_COLUMN_MAPPING
import tkinter as tk


def standardize_vehicle_number(vehicle_number: Any, length: int = 8) -> str:
    """Standardize the vehicle number to ensure it has the correct number of digits."""
    return str(vehicle_number).zfill(length)



def update_excel_row(
    df: pd.DataFrame,
    row_index: int,
    record: Dict[str, Any],
    rules_df: pd.DataFrame,
    rules_list: List[str],
) -> int:
    """Update Excel row with data from the record based on a mapping."""
    updates_made = 0
    for field, excel_col_index in EXCEL_COLUMN_MAPPING.items():
        if field in record:
            value_to_insert = str(record[field]).strip()  # Convert to string and strip whitespace
            if df.iat[row_index, excel_col_index] != value_to_insert:  # Check if the update is necessary
                df.iat[row_index, excel_col_index] = value_to_insert
                updates_made += 1
    if updates_made > 0:
        value_in_p_column = df.iat[row_index, 15]
        if value_in_p_column in rules_list:
            # Find the index of the matching value in the rules_list
            rules_row_index = rules_list.index(value_in_p_column)
            #print(f"Found matching value '{value_in_p_column}' at index {rules_row_index} in rules list")

            # Update the row with values from the rules_df based on RULES_COLUMN_MAPPING
            # the rules are letters mapping, example:     #H into V
                                                          #I into W
                                                          #F into X
                                                          #G into Y
            # its means, take the value from the column index H (rules_df) at the rules_row_index
            # and put it into the column index V (df) at the row_index
            for rule_from, rule_to in RULES_COLUMN_MAPPING.items():
                rules_col_index = ord(rule_from) - ord('A')  # Convert letter to 0-based index
                value_to_insert = rules_df.iat[rules_row_index, rules_col_index]
                excel_col_index = ord(rule_to) - ord('A')
                df.iat[row_index, excel_col_index] = value_to_insert
        else:
            print(f"Value '{reverse_word_if_hebrew(value_in_p_column)}' not found in rules list")
            
            
                    
           
    return updates_made


def transfer_data_to_excel(
    file_path: str,
    text_data: List[Dict[str, Any]],
    rules_df: pd.DataFrame,
    rules_list: List[str],
    
) -> Tuple[int, int, List[str],pd.DataFrame]:
    """
    Transfer data to Excel based on provided text records and rules.

    Returns:
        Tuple containing:
            - Number of rows updated.
            - Total number of rows processed.
            - List of unmatched vehicle numbers.
            - Updated DataFrame.
    """
    try:
        df = pd.read_excel(file_path, dtype=str)
        vehicle_number_col_index = 10  # Adjust as needed for the correct column index for vehicle numbers

        # Add a standardized vehicle number column as key
        df['standardized_vehicle_number'] = df.iloc[:, vehicle_number_col_index].apply(standardize_vehicle_number)

        total_rows = 0
        rows_updated = 0
        unmatched_vehicles: List[str] = []

        # Iterate over each record
        for record in text_data:
            vehicle_number_from_record = record.get('vehicle_number', '').strip()
            row_indices = df.index[df['standardized_vehicle_number'] == vehicle_number_from_record].tolist()
            total_rows += 1

            if row_indices:
                for row_index in row_indices:
                    if update_excel_row(df, row_index, record, rules_df, rules_list) > 0:
                        rows_updated += 1
                    
                    if bad_owner(record,df,row_index):
                        df.at[row_index, 'BAD RECORD'] = True
            else:
                unmatched_vehicles.append(vehicle_number_from_record)

            # now we need to check if the ownership date inside the record, is smaller than the report date which is in the df
            # if it isnt, we create a new col called BAD RECORD and put the value inside to true
          #("ownership_date", 156, 6),
                        

        return rows_updated, total_rows, unmatched_vehicles,df

    except Exception as e:
        raise RuntimeError(f"Failed to update Excel file: {str(e)}")
    

def bad_owner(row_data,df : pd.DataFrame,row_index):
    
        ownership_date = row_data.get('ownership_date', '').strip()
        if ownership_date == '':
            return True
        if ownership_date == '000000':
            return True
        report_date = df.iat[row_index, 1]
     
    
        # Convert "Report Date" to datetime object
        report_date_clean = datetime.datetime.strptime(report_date, "%d.%m.%Y")
    
        # Convert "Ownership Date" to datetime object
        # Assuming the year is in the 2000s
        ownership_date_clean = datetime.datetime.strptime(ownership_date, "%d%m%y")
        #print after conversion
        
        if ownership_date_clean > report_date_clean:
            print(f"found bad: Report Date: {report_date_clean}, Ownership Date: {ownership_date_clean}")
            #add this value to the df at the row_index
            df.at[row_index, 'report_vs_owner'] = f"Report Date: {report_date_clean}, Ownership Date: {ownership_date_clean}"
            return True
        return False

