import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from src.FromMot.text_processing import parse_text_file
from src.FromMot.clean_records import process_record
from constants import EXTRACTION_FORMULA
from src.FromMot.data_to_excel_file import transfer_data_to_excel
from src.FromMot.file_handling import process_zip_files
import os

class MOTWindow:
    def __init__(self, root):
        self.root = root
        self.current_step = 0
        self.text_data = []
        self.excel_file_path = None  # Store the path to the Excel file
        self.setup_gui()

    def setup_gui(self):
        # Create a new top-level window
        self.window = tk.Toplevel(self.root)
        self.window.title("FROM MOT Processing/ממשרד התחבורה")
        self.window.geometry("600x400")
        self.window.grab_set()  # Make the window modal

        # Layout using grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=3)

        # Text widget for output
        self.output_text = scrolledtext.ScrolledText(self.window, height=10, width=50)
        self.output_text.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky='nsew')

        # Define buttons
        self.text_file_btn = ttk.Button(self.window, text="להעלות קובץ טקסט ", command=self.upload_text_file)
        self.text_file_btn.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.excel_file_btn = ttk.Button(self.window, text="להעלות קובץ אקסל ידוע פיתוח", command=self.upload_excel_file)
        self.excel_file_btn.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.zip_folder_btn = ttk.Button(self.window, text="היכן (תיקייה) של קבצי הזיפ", command=self.select_zip_folder)
        self.zip_folder_btn.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

        self.exit_btn = ttk.Button(self.window, text="סיום התכנית", command=self.exit_program)
        self.exit_btn.grid(row=3, column=0, padx=10, pady=10, sticky='ew')
        self.exit_btn.config(state='disabled')  # Initially disabled

        self.update_button_states()

    def update_button_states(self):
        states = ['normal', 'disabled']
        self.text_file_btn.config(state=states[self.current_step != 0])
        self.excel_file_btn.config(state=states[self.current_step != 1])
        self.zip_folder_btn.config(state=states[self.current_step != 2])
        self.exit_btn.config(state=states[self.current_step != 3])

    def upload_text_file(self):
        file_path = filedialog.askopenfilename(title="בחר את קובץ הטקסט ממשרד התחבורה", filetypes=[("Text files", "*.txt")])
        if file_path:
            encodings = ['utf-8', 'windows-1255', 'iso-8859-8']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        self.text_data = parse_text_file(file)
                        self.output_text.insert(tk.END, "קובץ הטקסט נטען בהצלחה.\n")
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

        file_path = filedialog.askopenfilename(title="Open Excel file\קובץ יידוע לפיתוח", filetypes=[("Excel files", "*.xls *.xlsx")])
        if file_path:
            ## saving the path to the excel file 
            self.excel_file_path = file_path
            transfer_data_to_excel(file_path, self.text_data, self.output_text)
            self.output_text.insert(tk.END, "קובץ האקסל נטען ועובד בהצלחה.\n")
            self.current_step = 2
            self.update_button_states()

    def select_zip_folder(self):
        if self.current_step != 2:
            messagebox.showerror("Step Error", "Please upload the Excel file first!")
            return
        folder_path = filedialog.askdirectory(title="Select the folder with ZIP files\התיקייה בה נמצאים קבצי הזיפ")
        if folder_path:
            process_zip_files(folder_path,self.excel_file_path,self.output_text)
            self.output_text.insert(tk.END, "ZIP folder processed successfully.\n")
            self.current_step = 3
            self.update_button_states()

    def exit_program(self):
            if messagebox.askyesno("פתיחת התיקייה עם קובץ האקסל", "לפתוח את התיקייה המכילה את קובץ האקסל?"):
                folder_path = os.path.dirname(self.excel_file_path)
                os.startfile(folder_path)
            self.window.destroy()

def open_from_mot_window(root):
    MOTWindow(root)

