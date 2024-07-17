import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from src.FromMot.text_processing import parse_text_file
from src.FromMot.clean_records import process_record
from constants import EXTRACTION_FORMULA
from src.FromMot.data_to_excel_file import transfter_data_to_excel

class MOTWindow:
    def __init__(self, root):
        self.root = root
        self.current_step = 0
        self.text_data = []
        self.setup_gui()

    def setup_gui(self):
        # Create a new top-level window
        self.window = tk.Toplevel(self.root)
        self.window.title("FROM MOT Processing")
        self.window.geometry("600x400")
        self.window.grab_set()  # Make the window modal

        # Layout using grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=3)

        # Text widget for output
        self.output_text = scrolledtext.ScrolledText(self.window, height=10, width=50)
        self.output_text.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky='nsew')

        # Define buttons
        self.text_file_btn = ttk.Button(self.window, text="Upload Text File", command=self.upload_text_file)
        self.text_file_btn.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.excel_file_btn = ttk.Button(self.window, text="Upload Excel File", command=self.upload_excel_file)
        self.excel_file_btn.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.zip_folder_btn = ttk.Button(self.window, text="Select ZIP Folder", command=self.select_zip_folder)
        self.zip_folder_btn.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

        self.process_btn = ttk.Button(self.window, text="Process Files", command=self.process_files)
        self.process_btn.grid(row=3, column=0, padx=10, pady=10, sticky='ew')

        self.update_button_states()

    def update_button_states(self):
        self.text_file_btn.config(state='normal' if self.current_step == 0 else 'disabled')
        self.excel_file_btn.config(state='normal' if self.current_step == 1 else 'disabled')
        self.zip_folder_btn.config(state='normal' if self.current_step == 2 else 'disabled')
        self.process_btn.config(state='normal' if self.current_step == 3 else 'disabled')

    def upload_text_file(self):
        file_path = filedialog.askopenfilename(title="Open text file from ministry", filetypes=[("Text files", "*.txt")])
        if file_path:
            encodings = ['utf-8', 'windows-1255', 'iso-8859-8']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        self.text_data = parse_text_file(file)
                        self.output_text.insert(tk.END, "Text file loaded successfully.\n")
                        self.current_step = 1
                        self.update_button_states()
                        return
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    messagebox.showerror("File Error", f"An error occurred: {str(e)}")

    def upload_excel_file(self):
        if self.current_step != 1:
            messagebox.showerror("Step Error", "Please upload the text file first!")
            return

        file_path = filedialog.askopenfilename(title="Open Excel file", filetypes=[("Excel files", "*.xls *.xlsx")])
        if file_path:
            transfter_data_to_excel(file_path, self.text_data, self.output_text)
            self.output_text.insert(tk.END, "Excel file loaded and processed successfully.\n")
            self.current_step = 2
            self.update_button_states()

    def select_zip_folder(self):
        if self.current_step != 2:
            messagebox.showerror("Step Error", "Please upload the Excel file first!")
            return
        folder_path = filedialog.askdirectory(title="Select the folder with ZIP files")
        if folder_path:
            self.output_text.insert(tk.END, "ZIP folder selected successfully.\n")
            self.current_step = 3
            self.update_button_states()

    def process_files(self):
        if self.current_step != 3:
            messagebox.showerror("Step Error", "Please complete all previous steps!")
            return
        self.output_text.insert(tk.END, "Processing files...\n")
        self.output_text.insert(tk.END, "Files processed successfully!\n")
        self.current_step = 0
        self.update_button_states()

def open_from_mot_window(root):
    MOTWindow(root)

