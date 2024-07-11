
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from datetime import datetime
from src.ToMot.formula import apply_formula



from constants import COLUMN_A_INDEX, COLUMN_K_INDEX, FORMAT_CONFIG


def read_excel_file(file_path, cols=[COLUMN_A_INDEX,COLUMN_K_INDEX]):
    """ Read specified columns from the Excel file. """

    
    return pd.read_excel(file_path, usecols=cols)


def create_text_content(df):
    """ Apply the formula and create text content for the file. """
    today = datetime.today()
    formatted_data = [apply_formula(row, today, FORMAT_CONFIG) for index, row in df.iterrows()]
    return "\r\n".join(formatted_data) + "\r\n"

def save_text_file(content, filename='default_to_mot.txt'):
    """ Save the content to a text file with UTF-8 encoding and Windows CRLF. """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    messagebox.showinfo("Success", f"File '{filename}' saved successfully!")