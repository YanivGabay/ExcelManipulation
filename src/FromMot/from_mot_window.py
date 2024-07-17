import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from src.FromMot.text_processing import parse_text_file
from src.FromMot.clean_records import process_record
from constants import EXTRACTION_FORMULA
from src.FromMot.data_to_excel_file import transfter_data_to_excel

text_data = []

def open_from_mot_window(root):
    # State to track the current step
    current_step = 0
    
    # Create a new top-level window
    from_mot_window = tk.Toplevel(root)
    from_mot_window.title("FROM MOT Processing")
    from_mot_window.geometry("600x400")
    from_mot_window.grab_set()  # Make the window modal

    # Layout using grid
    from_mot_window.grid_columnconfigure(0, weight=1)
    from_mot_window.grid_columnconfigure(1, weight=3)

    # Text widget for output
    output_text = scrolledtext.ScrolledText(from_mot_window, height=10, width=50)
    output_text.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky='nsew')

    # Define buttons
    text_file_btn = ttk.Button(from_mot_window, text="Upload Text File", command=lambda: upload_text_file())
    text_file_btn.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

    excel_file_btn = ttk.Button(from_mot_window, text="Upload Excel File", command=lambda: upload_excel_file())
    excel_file_btn.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

    zip_folder_btn = ttk.Button(from_mot_window, text="Select ZIP Folder", command=lambda: select_zip_folder())
    zip_folder_btn.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

    process_btn = ttk.Button(from_mot_window, text="Process Files", command=lambda: process_files())
    process_btn.grid(row=3, column=0, padx=10, pady=10, sticky='ew')

    # Update button states based on the current step
    def update_button_states():
        text_file_btn.config(state='normal' if current_step == 0 else 'disabled')
        excel_file_btn.config(state='normal' if current_step == 1 else 'disabled')
        zip_folder_btn.config(state='normal' if current_step == 2 else 'disabled')
        process_btn.config(state='normal' if current_step == 3 else 'disabled')

    update_button_states()  # Initialize button states

    def upload_text_file():
    
        nonlocal current_step
        file_path = filedialog.askopenfilename(title="Open text file from ministry", filetypes=[("Text files", "*.txt")])
        if file_path:
            encodings = ['utf-8', 'windows-1255', 'iso-8859-8']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        text_data = parse_text_file(file)
                        output_text.insert(tk.END, "Text file loaded successfully.\n")
                        current_step = 1
                        update_button_states()
                        for record in text_data:
                        #print("Processing record")
                            if isinstance(record, dict):  # Ensure record is a dictionary
                                record = process_record(record, output_text)
                                print(f"record after beign clean:\n {record}")
                            else:
                                output_text.insert(tk.END, "Error: Record is not a dictionary.\n") 
                        return
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    messagebox.showerror("File Error", f"An error occurred: {str(e)}")

    def upload_excel_file():
        nonlocal current_step
        if current_step != 1:
            messagebox.showerror("Step Error", "Please upload the text file first!")
            return

        file_path = filedialog.askopenfilename(title="Open Excel file", filetypes=[("Excel files", "*.xls *.xlsx")])
        if not file_path:
            messagebox.showinfo("Info", "No file selected!")
            return  

        try:
            # Assuming transfter_data_to_excel handles all logic internally
            transfter_data_to_excel(file_path, text_data, output_text)
            current_step = 2
            update_button_states()
            output_text.insert(tk.END, "Excel file loaded and processed successfully.\n")
        except Exception as e:
            messagebox.showerror("Excel Loading Error", f"Failed to load or process Excel file: {str(e)}")
            current_step -= 1  # Decrement the step count
            update_button_states()

    def select_zip_folder():
        nonlocal current_step
        if current_step != 2:
            messagebox.showerror("Step Error", "Please upload the Excel file first!")
            return
        folder_path = filedialog.askdirectory(title="Select the folder with ZIP files")
        if folder_path:
            output_text.insert(tk.END, "ZIP folder selected successfully.\n")
            current_step = 3
            update_button_states()

    def process_files():
        nonlocal current_step
        if current_step != 3:
            messagebox.showerror("Step Error", "Please complete all previous steps!")
            return
        output_text.insert(tk.END, "Processing files...\n")
        # Here, add your file processing logic
        output_text.insert(tk.END, "Files processed successfully!\n")
        current_step = 0  # Reset the steps if needed
        update_button_states()

    # Initially disable all buttons except the first
    update_button_states()

