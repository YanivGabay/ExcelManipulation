
from tkinter import filedialog, messagebox, ttk

from src.ToMot.file_handling import read_excel_file, create_text_content, save_text_file

from datetime import datetime

def load_to_mot():
    messagebox.showinfo("Info" , "בבקשה לבחור את טופס מכתב ידוע לפיתוח")
    file_path = filedialog.askopenfilename(title="Select the Excel file",
                                           filetypes=[("Excel files", "*.xls"), ("Excel files", "*.xlsx")])
    if not file_path:
        messagebox.showinfo("Info", "No file selected!")
        return
    
    try:
        # Read the Excel file
        df = read_excel_file(file_path)
        # Create the text content
        content = create_text_content(df)
        # Get the file name
     
        file_name = f"to_mot_{datetime.now().strftime('%Y%m%d')}.txt"
                                                 
        if file_name:
            save_text_file(content, file_name)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")