import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from src.FromMot.text_processing import parse_text_file
from src.FromMot.clean_records import process_record
from constants import EXTRACTION_FORMULA

def open_from_mot_window(root):
    # Create a new top-level window
    from_mot_window = tk.Toplevel(root)
    from_mot_window.title("FROM MOT Processing")
    from_mot_window.geometry("600x400")
    from_mot_window.grab_set()  # This line makes the window modal
    # Layout using grid
    from_mot_window.grid_columnconfigure(0, weight=1)
    from_mot_window.grid_columnconfigure(1, weight=3)

    # Buttons for file uploads
    ttk.Button(from_mot_window, text="Upload Text File/להעלות את קובץ הטקסט ממשרד התחבורה", command=lambda: upload_text_file()).grid(row=0, column=0, padx=10, pady=10, sticky='ew')
    ttk.Button(from_mot_window, text="Upload Excel File/להעלות את קובץ ידוע לפיתוח", command=lambda: upload_excel_file()).grid(row=1, column=0, padx=10, pady=10, sticky='ew')
    ttk.Button(from_mot_window, text="Select ZIP Folder/תיקייה היכן שקבצי הזיפ נמצאים", command=lambda: select_zip_folder()).grid(row=2, column=0, padx=10, pady=10, sticky='ew')
    ttk.Button(from_mot_window, text="Process Files/לחצו כאן להתחיל", command=lambda: process_files()).grid(row=3, column=0, padx=10, pady=10, sticky='ew')

    # Text widget for output
    output_text = scrolledtext.ScrolledText(from_mot_window, height=10, width=50)
    output_text.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky='nsew')

    # Define the file upload functions
    def upload_text_file():
        file_path = filedialog.askopenfilename(title="Open text file from ministry", filetypes=[("Text files", "*.txt")])
        encodings = ['utf-8', 'windows-1255', 'iso-8859-8']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    # Clear the Treeview
                
                    text_data = parse_text_file(file)
                    output_text.insert(tk.END,f"finished loading the text file from ministry")

                    for record in text_data:
                    #print("Processing record")
                        if isinstance(record, dict):  # Ensure record is a dictionary
                            record = process_record(record, output_text)
                            print(f"record after beign clean:\n {record}")
                        else:
                            output_text.insert(tk.END, "Error: Record is not a dictionary.\n") 
            except UnicodeDecodeError:
                # This exception will trigger if the encoding is incorrect
                continue  # Try the next encoding
            except FileNotFoundError:
                output_text.delete('1.0', tk.END)
                output_text.insert(tk.END, "Error: File not found.")
                return  # Exit the function
            except Exception as e:
                output_text.delete('1.0', tk.END)
                output_text.insert(tk.END, f"Error reading file: {e}")
                return  # Exit the function

        if file_path:
            output_text.insert(tk.END, f"Loaded text file: {file_path}\n")
        
   
    
    def upload_excel_file():
        file_path = filedialog.askopenfilename(title="Open Excel file (מכתב יידוע לפיתוח)", filetypes=[("Excel files", "*.xls *.xlsx")])
        if file_path:
            output_text.insert(tk.END, f"Loaded Excel file: {file_path}\n")

    def select_zip_folder():
        folder_path = filedialog.askdirectory(title="Select the folder with ZIP files")
        if folder_path:
            output_text.insert(tk.END, f"Selected ZIP folder: {folder_path}\n")

    def process_files():
        # Placeholder for processing logic
        output_text.insert(tk.END, "Starting file processing...\n")
        # Add your processing code here
        output_text.insert(tk.END, "Files processed successfully!\n")

