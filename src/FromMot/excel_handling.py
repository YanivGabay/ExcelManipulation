
import os
import pandas as pd

def write_excel_file(df, file_path):
    file_extension = os.path.splitext(file_path)[1]
    
    if file_extension == '.xls':
        engine = 'xlwt'  # for older Excel format
    elif file_extension == '.xlsx':
        engine = 'openpyxl'  # for newer Excel format
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")

    with pd.ExcelWriter(file_path, engine=engine) as writer:
        df.to_excel(writer, index=False)