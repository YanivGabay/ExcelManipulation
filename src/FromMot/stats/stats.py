import pandas as pd
from typing import List, Dict
from src.FromMot.stats.compute_distribution import compute_distribution

class StatsExcelExporter:
    def __init__(self, df: pd.DataFrame, output_path: str):
        self.df = df
        self.output_path = output_path.replace(".xlsx", "_stats.xlsx")

    def create_stats_excel(self):
        # Initial list of columns
        columns = self.df.columns.tolist()
        print(f"Original columns: {columns}")

        # Filter out columns with names containing 'Unnamed' or empty names
        filtered_columns = [col for col in columns if col and 'Unnamed' not in col]
        print(f"Filtered columns (excluding 'Unnamed' and empty names): {filtered_columns}")

        # Further filter to include only columns that have at least one non-NaN value
        valid_columns = [col for col in filtered_columns if self.df[col].notna().any()]
        print(f"Valid columns (with at least one non-NaN value): {valid_columns}")

        if not valid_columns:
            print("No valid columns found to export.")
            return  # Exit the method without creating an Excel file

        # Calculate distribution only on valid columns
        distribution = compute_distribution(self.df, valid_columns)

        with pd.ExcelWriter(self.output_path, engine='openpyxl') as writer:
            written_sheets = 0  # Counter to track if at least one sheet is written

            for column, data in distribution.items():
                # Only write non-empty data
                if not data.empty:
                    # Ensure sheet name is valid (Excel sheet names have restrictions)
                    sheet_name = self._sanitize_sheet_name(column)
                    data.to_excel(writer, sheet_name=sheet_name, index=True)
                    written_sheets += 1
                    print(f"Written sheet: {sheet_name}, Data:\n{data}")

            # Check if at least one sheet was written
            if written_sheets == 0:
                print("No non-empty data found in valid columns. No sheets were written.")
            else:
                print(f"Stats Excel file created at {self.output_path}")

    def _sanitize_sheet_name(self, name: str) -> str:

        # Excel sheet names must be <= 31 characters and cannot contain: : \ / ? * [ ]
        invalid_chars = [":", "\\", "/", "?", "*", "[", "]"]
        for char in invalid_chars:
            name = name.replace(char, "_")
        return name[:31]  # Truncate to 31 characters

