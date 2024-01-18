import tkinter as tk
from tkinter import filedialog, scrolledtext
import pandas as pd
from datetime import datetime
import os
import re
from tkinter import ttk

def display_file_contents(file_path):
    encodings = ['utf-8', 'windows-1255', 'iso-8859-8']  # List of encodings to try
    for encoding in encodings:
        try:
            ##### will insert to a tree view after i will properly read the file
            ##### and understand how to format the fields

            with open(file_path, 'r', encoding=encoding) as file:
                for line in file:
                    #words = line.strip().split(maxsplit=10)  # Adjust maxsplit based on your data
                    
                  
                    parsed_line = parse_line(line)
                    reversed=[reverse_word_if_hebrew(word) for word in parsed_line]
                    tree.insert("", tk.END, values=reversed)
            
            with open(file_path, 'r', encoding=encoding) as file:
                processed_lines = []
                for line in file:
                    words = line.strip().split()  # Split line by spaces
                    processed_line = ' '.join(reverse_word_if_hebrew(word) for word in words)
                    processed_lines.append(processed_line)
                contents = '\n'.join(processed_lines)
                
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, contents)
            break
        except UnicodeDecodeError:
            continue  # Try the next encoding
        except Exception as e:
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, f"Error reading file: {e}")
            break

def reverse_word_if_hebrew(word):
    return word[::-1] if is_hebrew(word) else word

def parse_line(line):
    parts = line.strip().split()
    
    # First Field
    first_field = parts[0]
    col1, col2 = first_field[:-1], first_field[-1]

    # Second Field (date)
    col3 = parts[1]

    # Third Field
    third_field = parts[2]
    col4, col5 = third_field[:-1], third_field[-1]

    # Fourth and Fifth Fields
    long_number = parts[3]
    col6, col7, col8 = long_number[:8], long_number[8:15], long_number[15:]

    # Remaining Fields
    

    parsed_fields = [col1, col2, col3, col4, col5, col6, col7, col8] 
    print(parts[4:])  # Print the parsed fields for debugging
    return parsed_fields


def load_file():
    file_path = filedialog.askopenfilename()
    display_file_contents(file_path)

def load_file_auto():
    current_date = datetime.now().strftime("%y%m%d")
    #file_name = f"GuardWayFrom_MOT_{current_date}.txt"
    file_name = f"GuardWayFrom_MOT_07032021.txt"
    file_path = os.path.join(os.getcwd(), file_name)  # Assumes file is in the current working directory
    if os.path.exists(file_path):
        display_file_contents(file_path)
    else:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, "File not found.")
def is_hebrew(s):
    return bool(re.search('[\u0590-\u05FF]', s))



def setup_treeview():
    tree = ttk.Treeview(root)
    tree["columns"] = ("column1", "column2", "column3", "column4", "column5", "column6"
                       , "column7", "column8", "column9", "column10", "column6")  # Define your columns

    # Format columns
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("column1", anchor=tk.W, width=100)
    tree.column("column2", anchor=tk.W, width=100)
    # Add more columns as needed, setting their width and anchor

    # Create headings (Optional, for better readability)
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("column1", text="Column 1", anchor=tk.W)
    # Add headings for additional columns

    return tree

# Set up the GUI
root = tk.Tk()
root.title("Text File Viewer")

 

load_button = tk.Button(root, text="Load File Manually", command=load_file)
load_button.pack()

auto_load_button = tk.Button(root, text="Load Today's File", command=load_file_auto)
auto_load_button.pack()
tree = setup_treeview()
tree.pack(expand=True, fill='both')
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=200, height=5)
text_area.pack(padx=10, pady=10)

root.mainloop()
