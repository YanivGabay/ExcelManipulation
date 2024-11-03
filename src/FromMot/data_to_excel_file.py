import pandas as pd
from tkinter import messagebox
from typing import Any, Dict, List, Tuple
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
        # Check if the value in column 'P' matches any value in the rules_list
        try:
            p_column_loc = df.columns.get_loc("P")
            value_in_p_column = df.iat[row_index, p_column_loc]
        except KeyError:
            raise ValueError("Column 'P' not found in the Excel file.")
        
        if value_in_p_column in rules_list:
            # Find the index of the matching value in the rules_list
            rules_row_index = rules_list.index(value_in_p_column)

            # Update the row with values from the rules_df based on RULES_COLUMN_MAPPING
            for original_column, rules_col_index in RULES_COLUMN_MAPPING.items():
                try:
                    original_col_loc = df.columns.get_loc(original_column)
                    df.iat[row_index, original_col_loc] = rules_df.iat[rules_row_index, rules_col_index]
                except KeyError:
                    raise ValueError(f"Column '{original_column}' not found in the Excel file.")
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
            else:
                unmatched_vehicles.append(vehicle_number_from_record)

     
                        

        return rows_updated, total_rows, unmatched_vehicles,df

    except Exception as e:
        raise RuntimeError(f"Failed to update Excel file: {str(e)}")