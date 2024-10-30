import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from src.FromMot.text_processing import parse_text_file
from src.FromMot.clean_records import process_record
from constants import EXTRACTION_FORMULA
from src.FromMot.data_to_excel_file import transfer_data_to_excel
from src.FromMot.file_handling import process_zip_files
import os
import pandas as pd

class MOTWindow:
    def __init__(self, root):
        self.root = root
        self.current_step = 0
        self.text_data = []
        self.excel_file_path = None  # Store the path to the Excel file
        self.output_folder = None  # Store the path to the output folder
        self.setup_gui()
        self.export_window = None
        self.column_vars = {}
        self.rules_df = None

    def setup_gui(self):
        # Create a new top-level window
        self.window = tk.Toplevel(self.root)
        self.window.title("FROM MOT Processing/ממשרד התחבורה")
        self.window.geometry("600x400")
        self.window.grab_set()  # Make the window modal

        #load an excel file into a dataframe
        # name will always be:סיווג עבירות למכתב.xlsx
        # on the same folder as the script
        self.rules_df = pd.read_excel('סיווג עבירות למכתב.xlsx')
        if self.rules_df.empty:
            
            messagebox.showerror("Error", "אין קובץ סיווג עבירות למכתב.xlsx בתיקיית הסקריפט")
            return
        
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

        self.export_btn = ttk.Button(self.window, text="לייצא נתונים", command=self.export_window)
        self.export_btn.grid(row=3, column=0, padx=10, pady=10, sticky='ew')
        self.export_btn.config(state='disabled')

        self.exit_btn = ttk.Button(self.window, text="סיום התכנית", command=self.exit_program)
        self.exit_btn.grid(row=4, column=0, padx=10, pady=10, sticky='ew')
        self.exit_btn.config(state='disabled')  # Initially disabled

        self.update_button_states()

    def update_button_states(self):
        states = ['normal', 'disabled']
        self.text_file_btn.config(state=states[self.current_step != 0])
        self.excel_file_btn.config(state=states[self.current_step != 1])
        self.zip_folder_btn.config(state=states[self.current_step != 2])
        self.export_btn.config(state=states[self.current_step != 3])
        self.exit_btn.config(state=states[self.current_step != 4])

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
            self.output_folder = os.path.dirname(file_path)
            
            transfer_data_to_excel(file_path, self.text_data, self.output_text,self.rules_df)
           
           
           
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

    def export_window(self):
        self.export_window = tk.Toplevel(self.window)
        self.export_window.title("Export Data")
        self.export_window.geometry("800x500")

        try:
          df = pd.read_excel(self.excel_file_path)
        except Exception as e:
          messagebox.showerror("Error", "Failed to load Excel file: " + str(e))
          return
        # Frame for checkboxes
        canvas = tk.Canvas(self.export_window)
        scrollbar = tk.Scrollbar(self.export_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Configure the canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Packing canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        default_checked_indices = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,27}  # Change this set to match your default selections by index

    # Creating a checkbox for each column
        
        for index, column in enumerate(df.columns):
            is_checked = index in default_checked_indices  # Only check if the index is in the preset list
            var = tk.BooleanVar(value=is_checked)
            chk = tk.Checkbutton(scrollable_frame, text=column, variable=var)
            chk.pack(anchor='w')
            self.column_vars[column] = var
            self.column_vars[column] = var
            
        # Export button
        export_btn = ttk.Button(self.export_window, text="Export Selected Columns", command=lambda: self.export_selected_columns(df))
        export_btn.pack(pady=10)


        

    def export_selected_columns(self, df):
        selected_columns = [column for column, var in self.column_vars.items() if var.get()]
        if selected_columns:
            # Extract selected columns and export
            data_to_export = df[selected_columns]
            today = pd.Timestamp.today().strftime("%Y-%m-%d")
            new_file_name = f"selected_columns_export_{today}.xlsx"
            export_path = os.path.join(os.path.dirname(self.excel_file_path), new_file_name)
            data_to_export.to_excel(export_path, index=False)
            messagebox.showinfo("ייצוא הקובץ בוצע בהצלחה", "העמודות הנבחרות יוצאו בהצלחה")
            # Optionally open the folder
            if messagebox.askyesno("פתיחת התיקייה", "האם מעוניין שאפתח את התיקייה שבה נשמר הקובץ?"):
                os.startfile(os.path.dirname(export_path))
                    # Close the export window and return focus to the main window
            self.current_step = 4
            self.update_button_states()
            self.export_window.destroy()
            self.window.focus_set()
        else:
            messagebox.showerror("Export Error", "Please select one or more columns to export.")

    def exit_program(self):
            if messagebox.askyesno("פתיחת התיקייה עם קובץ האקסל", "לפתוח את התיקייה המכילה את קובץ האקסל?"):
                folder_path = os.path.dirname(self.excel_file_path)
                os.startfile(folder_path)
            self.window.destroy()

def open_from_mot_window(root):
    MOTWindow(root)

