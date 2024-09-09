from tkinter import filedialog, messagebox, ttk
import os
from src.ToMot.file_handling import read_excel_file, create_text_content, save_text_file
from datetime import datetime

def load_to_mot():
    messagebox.showinfo("Info", "בבקשה לבחור את טופס מכתב ידוע לפיתוח")
    file_path = filedialog.askopenfilename(title="לבחור את קובץ",
                                           filetypes=[("Excel files", "*.xls"), ("Excel files", "*.xlsx")])
    if not file_path:
        messagebox.showinfo("Info", "No file selected!")
        return
    
    try:
        # Read the Excel file
        df = read_excel_file(file_path)
        # Create the text content
        content = create_text_content(df)
        # Determine the directory of the Excel file and the file name
        directory = os.path.dirname(file_path)
        file_name = f"to_mot_{datetime.now().strftime('%Y%m%d')}.txt"
        full_path = os.path.join(directory, file_name)
        
        # Save the text file in the same directory as the Excel file
        save_text_file(content, full_path)
        
        # Ask if the user wants to open the folder
        if messagebox.askyesno("Open Folder", "האם לפתוח את התיקייה בה נשמר קובץ למשרד התחבורה?"):
            os.startfile(directory)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
