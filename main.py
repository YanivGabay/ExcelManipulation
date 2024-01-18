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

extraction_specs = [
    # (column_name, start_position, length)
    ("costumer_code", 1, 3),
    ("response_code", 4, 1),
    ("series", 5, 1),
    ("filler", 6, 6),
    ("date", 12, 6),
    ("hour", 18, 4),
    ("adress", 42, 6),
      ("type_of_ownership", 48, 1),
      ("handicap", 49, 1),
       ("number_of_offend", 50, 4),
        ("number_of_offend", 54, 3),
         
    ("trial_date", 57, 6),
    ("pusher", 63, 4),
    ("vehicle_number", 67, 8),
    ("postal_code", 75, 7),
    ("city_code", 82, 4),
    ("city_name", 86, 13),
    # "city_name_corrected" would be used when we know what @mmm(R2) does
    ("street_name", 99, 17),
    # "street_name_corrected" would be used when we know what @mmm(T2) does
    ("house_number", 116, 5),
    ("apartment_number", 121, 4),
    ("family", 125, 14),
    # "family_corrected" would be used when we know what @mmm(X2) does
    ("private", 139, 8),
    # "private_corrected" would be used when we know what @mmm(Z2) does
    ("identity", 147, 9),
    ("ownership_date", 156, 6),
    ("vehicle_type", 162, 3),
    # "vehicle_type_description" might be used for the next three, but need more context to differentiate them
    ("vehicle_type_description1", 165, 7),
    ("logo_where", 172, 5),
    ("name_of_where", 177, 14),
    # "vehicle_type_description_corrected" would be used when we know what @mmm(AH2) does
    ("color", 191, 2),
    ("code_of_note", 193, 1),
    # "manufacturer_name_corrected" would be used when we know how to handle the duplicate names
    ("production_year", 194, 2),
    ("expiry", 196, 6),
    # We will need to handle the CONCATENATE function separately
]




def parse_line(line):
    #temp = line
    extracted_values = []
    for field_name, start, length in extraction_specs:
        print(extract_mid(line, start, length))
        extracted_values.append(extract_mid(line, start, length))
    
    return extracted_values
   

def extract_mid(text, start_position, length):
    # Adjusting start_position to be zero-indexed (Python starts counting from 0)
    adjusted_start = start_position - 1

    # Extracting and returning the substring
    return text[adjusted_start:adjusted_start + length]

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



def setup_treeview(frame):
    # Create the treeview inside the given frame
    tree = ttk.Treeview(frame)
    
    # Define the columns based on the extraction_specs
    column_ids = [spec[0] for spec in extraction_specs]
    tree['columns'] = column_ids
    
    # Configure the columns
    for col_id in column_ids:
        tree.heading(col_id, text=col_id)
        tree.column(col_id, anchor=tk.W, width=100, stretch=False)  # Set stretch=False
    
    return tree

# Set up the main GUI window
root = tk.Tk()
root.title("Text File Viewer")

# Set the initial size and maximum size of the window
root.geometry('800x600')  # Initial size of the window
root.maxsize(1200, 800)   # Maximum size of the window
# Create a frame to hold the Treeview and scrollbars


# Main frame
main_frame = ttk.Frame(root)
main_frame.pack(fill='both', expand=True)

# Top frame for buttons and text box
top_frame = ttk.Frame(main_frame)
top_frame.pack(side='top', fill='x')

load_button = tk.Button(top_frame, text="Load File Manually", command=load_file)
load_button.pack(side='left', padx=10, pady=10)

auto_load_button = tk.Button(top_frame, text="Load Today's File", command=load_file_auto)
auto_load_button.pack(side='left', padx=10)

text_area = scrolledtext.ScrolledText(top_frame, wrap=tk.WORD, width=80, height=5)
text_area.pack(side='left', fill='x', expand=True, padx=10, pady=10)

# Bottom frame for Treeview and scrollbars
bottom_frame = ttk.Frame(main_frame)
bottom_frame.pack(fill='both', expand=True)

# Setup the Treeview
tree = setup_treeview(bottom_frame)

# Create a Scrollbar for the y-axis
y_scroll = ttk.Scrollbar(bottom_frame, orient="vertical", command=tree.yview)
y_scroll.pack(side='right', fill='y')
tree.configure(yscrollcommand=y_scroll.set)

# Create a Scrollbar for the x-axis
x_scroll = ttk.Scrollbar(bottom_frame, orient="horizontal", command=tree.xview)
x_scroll.pack(side='bottom', fill='x')
tree.configure(xscrollcommand=x_scroll.set)

# Pack the treeview
tree.pack(side='left', fill='both', expand=True)

root.mainloop()
