from tkinter import filedialog
import os
from datetime import datetime
import utilities as util
import pandas as pd
import re
import tkinter as tk
from tkinter import ttk
import gui_components as gui_comp
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

                
                postal_code_col_index = find_column_index(tree, "postal_code")
                if postal_code_col_index != -1:
                  process_postal_codes(tree, postal_code_col_index)
                else:
                   print("Postal code column not found")


                

                private_col_index = find_column_index(tree, "private")
                family_col_index = find_column_index(tree, "family")
                if private_col_index and family_col_index  != -1:
                  update_with_combined_values(tree, private_col_index, family_col_index)
                else:
                   print("Private or family column not found")

                street_name_col_index = find_column_index(tree, "street_name")
                if street_name_col_index != -1:
                 update_address_po_box(tree, street_name_col_index, "address_po_box")   
                else:
                   print("street_name column not found")
                   
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, f"Error reading file: {e}")
            break
def find_column_index(tree, column_name):
    columns = tree["columns"]
    if column_name in columns:
        return columns.index(column_name)
    return -1  # or handle the error as appropriate

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

def add_full_name(tree):
    for item in tree.get_children():
        # Get the current value of the postal code
        family = tree.item(item, 'values')[12]
        private = tree.item(item, 'values')[13]
        
        full_name = family + private 
        current_values = list(tree.item(item, 'values'))
        current_values[12] = full_name
        tree.item(item, values=current_values)

def parse_line(line):
   #temp = line
    extracted_values = []
    for field_name, start, length in util.extraction_specs:
        #print(extract_mid(line, start, length))
        extracted_values.append(util.extract_mid(line, start, length))
    
    return extracted_values

def process_postal_codes(tree, postal_code_col):
    
    for item in tree.get_children():
        # Get the current value of the postal code
        postal_code = tree.item(item, 'values')[postal_code_col]

        # Check for all-zero postal codes and mark them
        if postal_code == '0000000':
            tree.item(item, tags=('zero_postal_code',))
            tree.tag_configure('zero_postal_code', background='#D19191', foreground='white')

        else:
            # Process non-zero postal codes
            # Assuming 7-digit postal code
            postal_code = postal_code[2:] + postal_code[:2]

            # Update the postal code in the Treeview
            current_values = list(tree.item(item, 'values'))
            current_values[postal_code_col] = postal_code
            tree.item(item, values=current_values)

   

def update_address_po_box(tree, street_name_col, address_po_box_col):
    for item in tree.get_children():
        row_data = list(tree.item(item, 'values'))
        street_name = row_data[street_name_col]

        # Regex pattern to match 'תד', 'ת.ד', or 'ת"ד', followed by numbers
        po_box_pattern = r'ת.*ד.*?(\d+)'

        match = re.search(po_box_pattern, street_name)
        if match:
            po_box_number = match.group(1)  # Extract the number
        else:
            po_box_number = ''  # No match found

        # Update the row with the PO Box number
        row_data.append(po_box_number)
        tree.item(item, values=row_data)




def setup_treeview(frame, extraction_specs):
    tree = ttk.Treeview(frame)

    # Define the columns based on the extraction_specs
    column_ids = [spec[0] for spec in extraction_specs]
    tree['columns'] = column_ids

    # Add a combined column for the family and private columns
    combined_col_name = "combined_private_family"
    tree['columns'] = list(tree['columns']) + [combined_col_name]

    address_po_box_col = "address_po_box"
    tree['columns'] = list(tree['columns']) + [address_po_box_col]
    # Configure the columns
    for col_id in column_ids:
        tree.heading(col_id, text=col_id)
        tree.column(col_id, anchor=tk.W, width=100, stretch=False)

    tree.heading(combined_col_name, text="FullName")
    tree.column(combined_col_name, anchor=tk.W, width=100, stretch=False)
    tree.heading(address_po_box_col, text="Address PO Box")
    tree.column(address_po_box_col, anchor=tk.W, width=100, stretch=False)   

    return tree



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


def update_with_combined_values(tree, private_col, family_col):
    for item in tree.get_children():
        row_data = list(tree.item(item, 'values'))

        private_value = row_data[private_col].strip()  # Remove leading/trailing spaces
        family_value = row_data[family_col].strip()    # Remove leading/trailing spaces

        # Combine the values
        combined_value = private_value + " " + family_value

        # Update the row with the combined value
        row_data.append(combined_value)
        tree.item(item, values=row_data)
