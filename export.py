import tkinter as tk    
import pandas as pd

def save_to_excel(tree, filename, textbox):
    try:
        save_treeview_as_excel(tree, filename)
        textbox.delete('1.0', tk.END)
        textbox.insert(tk.END, "File saved successfully.")
    except Exception as e:
        textbox.delete('1.0', tk.END)
        textbox.insert(tk.END, f"Error reading file: {e}")


def save_treeview_as_excel(tree, filename):
    # Extracting the column names
    columns = tree['columns']

    # Creating a list of dictionaries from the Treeview items
    data = []
    for item in tree.get_children():
        row_data = tree.item(item, 'values')
        row_dict = dict(zip(columns, row_data))
        data.append(row_dict)

    # Creating a DataFrame and saving it as an Excel file
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
