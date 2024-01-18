from tkinter import filedialog
import os
from datetime import datetime
import utilities as util
import pandas as pd
import re
import tkinter as tk
from tkinter import ttk

def display_file_contents(file_path, tree, text_area):
    encodings = ['utf-8', 'windows-1255', 'iso-8859-8']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                processed_lines = []
                for line in file:
                    words = line.strip().split()  
                    processed_line = ' '.join(util.reverse_word_if_hebrew(word) for word in words)
                    processed_lines.append(processed_line)

                contents = '\n'.join(processed_lines)
                text_area.delete('1.0', tk.END)
                text_area.insert(tk.END, contents)
                
                file.seek(0)  # Reset file pointer to the beginning
                for line in file:
                    parsed_line = parse_line(line)
                    reversed = [util.reverse_word_if_hebrew(word) for word in parsed_line]
                    tree.insert("", tk.END, values=reversed)
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, f"Error reading file: {e}")
            break

def load_file(tree, text_area):
    file_path = filedialog.askopenfilename()
    display_file_contents(file_path, tree, text_area)

def load_file_auto(tree, text_area):
    current_date = datetime.now().strftime("%y%m%d")
    file_name = f"GuardWayFrom_MOT_{current_date}.txt"
    file_path = os.path.join(os.getcwd(), file_name)
    if os.path.exists(file_path):
        display_file_contents(file_path, tree, text_area)
    else:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, "File not found.")
def is_hebrew(s):
    return bool(re.search('[\u0590-\u05FF]', s))

def parse_line(line):
   #temp = line
    extracted_values = []
    for field_name, start, length in util.extraction_specs:
        #print(extract_mid(line, start, length))
        extracted_values.append(util.extract_mid(line, start, length))
    
    return extracted_values


def setup_treeview(frame, extraction_specs):
    tree = ttk.Treeview(frame)

    # Define the columns based on the extraction_specs
    column_ids = [spec[0] for spec in extraction_specs]
    tree['columns'] = column_ids

    # Configure the columns
    for col_id in column_ids:
        tree.heading(col_id, text=col_id)
        tree.column(col_id, anchor=tk.W, width=100, stretch=False)

    return tree