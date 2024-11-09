# src/main_gui.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from typing import Any, Dict, List, Optional
from src.FromMot.text_processing import parse_text_file
from src.FromMot.clean_records import process_record
from constants import EXTRACTION_FORMULA,NEW_COLUMN_NAMES
from src.FromMot.data_to_excel_file import transfer_data_to_excel
from src.FromMot.file_handling import process_zip_files
import os
import pandas as pd


class MOTWindow:
    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root
        self.current_step: int = 0
        self.text_data: List[Dict[str, Any]] = []
        self.excel_file_path: Optional[str] = None  # Store the path to the Excel file
        self.output_folder: Optional[str] = None  # Store the path to the output folder
        self.full_df: Optional[pd.DataFrame] =  None
        self.column_vars: Dict[str, tk.BooleanVar] = {}
        self.rules_df: Optional[pd.DataFrame] = None
        self.rules_list: List[str] = []
        
        self.setup_gui()

    def setup_gui(self) -> None:
        """Set up the GUI components."""
        # Create a new top-level window
        self.window: tk.Toplevel = tk.Toplevel(self.root)
        self.window.title("FROM MOT Processing/ממשרד התחבורה")
        self.window.geometry("600x400")
        self.window.grab_set()  # Make the window modal

        # Load an Excel file into a dataframe
        rules_file = 'סיווג עבירות למכתב.xlsx'
        if not os.path.exists(rules_file):
            messagebox.showerror("Error", f"File '{rules_file}' not found in the script directory.")
            self.window.destroy()
            return

        try:
            self.rules_df = pd.read_excel(rules_file)
            if self.rules_df.empty:
                messagebox.showerror("Error", f"File '{rules_file}' is empty.")
                self.window.destroy()
                return
            else:
                print(f"Rules file loaded successfully: {rules_file}")
                print(f"Columns: {self.rules_df.columns}")
                # Initialize output_text after rules are successfully loaded
                self.output_text = scrolledtext.ScrolledText(self.window, height=10, width=50)
                self.output_text.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky='nsew')
                # get all values from the B col into a list
              
                self.rules_list = self.rules_df.iloc[:,1].dropna().astype(str).tolist()
                self.output_text.insert(tk.END, "קובץ סיווג עבירות למכתב נטען בהצלחה.\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load '{rules_file}': {str(e)}")
            self.window.destroy()
            return

        # Layout using grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=3)

        # Define buttons
        self.text_file_btn: ttk.Button = ttk.Button(
            self.window, text="להעלות קובץ טקסט ", command=self.upload_text_file
        )
        self.text_file_btn.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.excel_file_btn: ttk.Button = ttk.Button(
            self.window, text="להעלות קובץ אקסל ידוע פיתוח", command=self.upload_excel_file
        )
        self.excel_file_btn.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.zip_folder_btn: ttk.Button = ttk.Button(
            self.window, text="היכן (תיקייה) של קבצי הזיפ", command=self.select_zip_folder
        )
        self.zip_folder_btn.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

        self.export_btn: ttk.Button = ttk.Button(
            self.window, text="לייצא נתונים", command=self.export_output
        )
        self.export_btn.grid(row=3, column=0, padx=10, pady=10, sticky='ew')
        self.export_btn.config(state='disabled')

        self.exit_btn: ttk.Button = ttk.Button(
            self.window, text="סיום התכנית", command=self.exit_program
        )
        self.exit_btn.grid(row=4, column=0, padx=10, pady=10, sticky='ew')
        self.exit_btn.config(state='disabled')  # Initially disabled

        self.update_button_states()

    def update_button_states(self) -> None:
        """Enable or disable buttons based on the current step."""
        states = ['normal', 'disabled']
        self.text_file_btn.config(state=states[self.current_step != 0])
        self.excel_file_btn.config(state=states[self.current_step != 1])
        self.zip_folder_btn.config(state=states[self.current_step != 2])
        self.export_btn.config(state=states[self.current_step != 3])
        self.exit_btn.config(state=states[self.current_step != 4])

    def upload_text_file(self) -> None:
        """Handle the upload of a text file."""
        file_path: str = filedialog.askopenfilename(
            title="בחר את קובץ הטקסט ממשרד התחבורה",
            filetypes=[("Text files", "*.txt")],
        )
        if file_path:
            encodings: List[str] = ['utf-8', 'windows-1255', 'iso-8859-8']
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
                    return
            messagebox.showerror("Encoding Error", "Failed to decode the text file with available encodings.")

    def upload_excel_file(self) -> None:
        """Handle the upload of an Excel file."""
        if self.current_step != 1:
            messagebox.showerror("Step Error", "Please upload the text file first!")
            return

        file_path: str = filedialog.askopenfilename(
            title="בחר קובץ אקסל ידוע פיתוח",
            filetypes=[("Excel files", "*.xls *.xlsx")],
        )
        if file_path:
            # Save the path to the Excel file
            self.excel_file_path = file_path
            self.output_folder = os.path.dirname(file_path)
            # Create an output folder in the file path
            output_folder_path = os.path.join(os.path.dirname(file_path), "output")
            os.makedirs(output_folder_path, exist_ok=True)
            self.output_folder = output_folder_path

            if self.rules_df is None:
                messagebox.showerror("Error", "קובץ סיווג עבירות למכתב לא נטען.")
                return

            # Transfer data to Excel
            try:
                rows_updated, total_rows, unmatched_vehicles,self.full_df = transfer_data_to_excel(
                    file_path,
                    self.text_data,
                    self.rules_df,
                    self.rules_list,
                    
                )
                if rows_updated > 0:
                    self.output_text.insert(
                        tk.END,
                        f"Excel file updated: {rows_updated} rows modified out of {total_rows} processed.\n"
                    )
                else:
                    self.output_text.insert(tk.END, "No rows modified.\n")
                
                if unmatched_vehicles:
                    self.output_text.insert(
                        tk.END,
                        f"Unmatched vehicles ({len(unmatched_vehicles)}): {', '.join(unmatched_vehicles)}\n"
                    )
                else:
                    self.output_text.insert(tk.END, "All vehicle numbers matched successfully.\n")
                
                self.current_step = 2
                self.update_button_states()
            except RuntimeError as e:
                messagebox.showerror("Excel Error", str(e))
                self.output_text.insert(tk.END, f"Error: {str(e)}\n")

    def select_zip_folder(self) -> None:
        """Handle the selection of a ZIP folder."""
        if self.current_step != 2:
            messagebox.showerror("Step Error", "Please upload the Excel file first!")
            return
        folder_path: str = filedialog.askdirectory(title="בחר את התיקייה של קבצי הזיפ")
        if folder_path:
            if self.excel_file_path is None:
                messagebox.showerror("Path Error", "Excel file path is not set.")
                return
            try:
                if self.full_df is not None and self.output_folder is not None:
                    self.full_df = process_zip_files(folder_path, self.full_df,self.output_folder)
                self.output_text.insert(tk.END, "ZIP folder processed successfully.\n")
                self.current_step = 3
                self.update_button_states()
            except Exception as e:
                messagebox.showerror("ZIP Processing Error", f"Failed to process ZIP files: {str(e)}")
                self.output_text.insert(tk.END, f"Error: {str(e)}\n")


    def export_output_file(self, df: pd.DataFrame) -> None:
              
        data_to_export: pd.DataFrame = df
        today: str = pd.Timestamp.today().strftime("%Y-%m-%d")
        new_file_name: str = f"output_{today}.xlsx"
         
        if self.output_folder is None:
            return
        export_path: str = os.path.join(self.output_folder, new_file_name)


        try:
            for column,new_name in NEW_COLUMN_NAMES.items():
                new_col_index = ord(column) - ord('A')  # Convert letter to 0-based index
                data_to_export.columns.values[new_col_index] = new_name
            data_to_export.to_excel(export_path, index=False)
            messagebox.showinfo("Success", "קובץ סופי יוצר בהצלחה.")
            
            # Optionally open the folder
            if messagebox.askyesno("Open Folder", "האם מעוניין שאפתח את התיקייה שבה נשמר הקובץ?"):
                os.startfile(os.path.dirname(export_path))
            
            # Close the export window and update state
            self.current_step = 4
            self.update_button_states()

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export columns: {str(e)}")
   
    def export_output(self) -> None:
        if self.full_df is None:
            messagebox.showerror("Error", "No data to export.")
            return
        self.export_output_file(self.full_df)
        

    def exit_program(self) -> None:
        """Exit the program, optionally opening the Excel file's directory."""
        if self.excel_file_path and messagebox.askyesno(
            "Open Folder",
            "האם מעוניין שאפתח את התיקייה המכילה את קובץ האקסל?"
        ):
            folder_path: str = os.path.dirname(self.excel_file_path)
            try:
                os.startfile(folder_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open folder: {str(e)}")
        self.window.destroy()
        #exit the program totally
        self.root.quit()



def open_from_mot_window(root: tk.Tk) -> None:
    """Function to open the MOTWindow."""
    MOTWindow(root)
