import tkinter as tk    
import pandas as pd
from tkinter import filedialog, messagebox, Toplevel, Checkbutton, Button

def save_to_excel(tree, filename, textbox):
    try:
        open_export_dialog(tree)
        textbox.delete('1.0', tk.END)
        textbox.insert(tk.END, "File saved successfully.")
    except Exception as e:
        textbox.delete('1.0', tk.END)
        textbox.insert(tk.END, f"Error reading file: {e}")

def open_export_dialog(tree):
    export_window = Toplevel()
    export_window.title("Export to Excel - Choose Cols to Export")
    check_boxes = {}

    checkboxes_frame = tk.Frame(export_window)
    checkboxes_frame.pack(fill='both', expand=True)

    num_cols = 2
    for idx, col in enumerate(tree['columns']):
        var = tk.BooleanVar()
        check_boxes[col] = var
        chk = Checkbutton(checkboxes_frame, text=col, variable=var)
        chk.grid(row=idx % (len(tree['columns']) // num_cols), column=idx // (len(tree['columns']) // num_cols), sticky='w')

    def export_data():
        selected_columns = [col for col, var in check_boxes.items() if var.get()]
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if filename:
            save_treeview_as_excel(tree, filename, selected_columns)
            export_window.destroy()

    def set_default():
        # Define your default columns here
        default_columns = ['Identifier', 'column2', 'column3']  # Replace with actual column names
        for col, var in check_boxes.items():
            var.set(col in default_columns)

    Button(export_window, text="Export", command=export_data).pack()
    Button(export_window, text="Default", command=set_default).pack()
    
def save_treeview_as_excel(tree, filename,selected_columns=None):
    # Extracting the column names
    if selected_columns is None:
     selected_columns = tree['columns']

    # Creating a list of dictionaries from the Treeview items
    data = []
    for item in tree.get_children():
        row_data = tree.item(item, 'values')
        # Only include data for selected columns
        row_dict = {col: row_data[idx] for idx, col in enumerate(tree['columns']) if col in selected_columns}
        data.append(row_dict)

    # Creating a DataFrame with selected columns and saving it as an Excel file
    df = pd.DataFrame(data, columns=selected_columns)
    df.to_excel(filename, index=False)
