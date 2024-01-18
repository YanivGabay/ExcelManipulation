import pandas as pd
from handleStrings import reverse_hebrew_strings,concatenate_columns
from excel_operations import read_xlsm_file




def main():
    file_path = 'ExampleFiles/From MOT converter.xlsm'  # Replace with your file path
    df = read_xlsm_file(file_path)

    if df is not None:
        # Displaying the first few rows of the DataFrame
        df = reverse_hebrew_strings(df)

        cols_to_drop = [col for col in df.columns if "מתוקן" in col]
        df.drop(columns=cols_to_drop, inplace=True)

        df = concatenate_columns(df, 'פרטי', 'משפחה', 'שם מלא')

        print(df.head(10))
        df.to_csv('output.csv', index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    main()

