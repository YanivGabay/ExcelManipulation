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
    file_loaded = False
    encodings = ['utf-8', 'windows-1255', 'iso-8859-8']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                # Clear the Treeview
                #tree.delete(*tree.get_children())
                text_data = parse_text_file(file)
                #debugg
                #number_of_records_to_print = 5  # You can adjust this number as needed
                #for i in range(min(number_of_records_to_print, len(text_data))):
                   #  print(f"Record {i + 1}: {text_data[i]}")
                    # print() 

                # Process each line in the file
                file_loaded = True
                text_area.delete('1.0', tk.END)
                text_area.insert(tk.END, "Found and read the Text file.")


                bad_records,highlighted_records,text_data = process_txt_file(text_data, text_area)
                transfer_data_to_tree(tree,text_data,bad_records,highlighted_records,text_area)

                text_area.delete('1.0', tk.END)
                text_area.insert(tk.END, "finished transfering data to the tree")
                #transfer data 
                #
                break  # Exit the loop if file is successfully processed
        except UnicodeDecodeError:
            # This exception will trigger if the encoding is incorrect
            continue  # Try the next encoding
        except FileNotFoundError:
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, "Error: File not found.")
            return  # Exit the function
        except Exception as e:
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, f"Error reading file: {e}")
            return  # Exit the function

    if not file_loaded:
        #if this delete will also delete text
        #need to check and fix if that the  case
        text = text_area.get("1.0", "end-1c")
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, "Error: Unable to read the file with the tried encodings. Latest warning: " + text)
        return
    
def transfer_data_to_tree(tree,text_data,bad_records,highlighted_records,text_area):
    print("Number of rows in the tree:", len(tree.get_children()))
    try:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, "Transfering data to the tree")
        for child in tree.get_children():
            #print("Processing tree child")  
            tree_item = tree.item(child)
            tree_address = tree_item['values'][find_tree_column_index(tree, 'Identifier')]
           # print("Tree Address:", tree_address)  # Debug print
           
            for record in text_data:
                #  print("Record Address:", record['address'])  # Debug print
                  if record['address'] == tree_address:
                        # Update necessary cells in the tree with data from record
                    update_tree_item(tree, child, record)
                    highlight_records(tree, child,highlighted_records)

                   
    except Exception as e:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, f"Error inside transfer_data_to_tree(): {e}")
             
def highlight_records(tree, item,highlighted_records):
    current_values = list(tree.item(item, 'values'))
    if current_values[0] in highlighted_records:
        tree.item(item, tags=('zero_postal_code',))
        tree.tag_configure('zero_postal_code', background='#D19191', foreground='white')

def update_tree_item(tree, item, record):
    current_values = list(tree.item(item, 'values'))

    for tree_column, record_field in util.column_to_field_mapping.items():
        if tree_column in tree['columns']:
            column_index = tree['columns'].index(tree_column)
            current_values[column_index] = record.get(record_field, '')
        


    tree.item(item, values=current_values)
    
def parse_text_file(file):
     text_data = []
     for line in file:
                    # Parse and reverse Hebrew words, then insert into the tree
        parsed_line = parse_line(line)
        reversed_line = [util.reverse_word_if_hebrew(word) for word in parsed_line]
        column_names = [spec[0] for spec in util.extraction_specs]
        #print(reversed_line)
        single_line_data = dict(zip(column_names, reversed_line))
        #print(single_line_data) 
        text_data.append(single_line_data)
     return text_data               
def proccess_record(record,text_area,bad_records,highlighted_records):

   try:
    record = proccess_postal_codes(record,highlighted_records,text_area)

  
    record = proccess_full_name(record,bad_records,text_area)

  
    record = proccess_street_name(record,bad_records,text_area)
    #print(record)
    return record
   except Exception as e:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, f"Error inside Process_record(): {e}")

   

def process_txt_file(text_data, text_area): 
    bad_records = []
    highlighted_records = []
    try:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, "Cleaning the data")
        for record in text_data:
             if isinstance(record, dict):  # Ensure record is a dictionary
                  record = proccess_record(record, text_area, bad_records, highlighted_records)
             else:
                  text_area.insert(tk.END, "Error: Record is not a dictionary.\n")
             break  # Skip this record and continue with the next

    except Exception as e:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, f"Error process_txt_file: {e}")

    return bad_records,highlighted_records,text_data 
def proccess_postal_codes(record,highlighted_records,text_area):

       
        postal_code = record["postal_code"]
        if postal_code == '0000000':
            record["postal_code"] = 'zeros'
            highlighted_records.append(record["address"])
            
            
        else:
            # Process non-zero postal codes
            # Assuming 7-digit postal code
            postal_code = postal_code[2:] + postal_code[:2]
            record["postal_code"] = postal_code
    
        return record      
  
def proccess_full_name(record,bad_records,text_area): 
    first_name = record.get('private', '').strip()
    last_name = record.get('family', '').strip()
    record['full_name'] = f"{first_name} {last_name}"
    return record
    
    #future check for insertiong into bad records
    

   
def proccess_street_name(record,bad_records,text_area):
    
    street_name = record.get('street_name', '').strip()
    # Regex pattern to match 'תד', 'ת.ד', or 'ת"ד', followed by numbers
    po_box_pattern = r'ת.*ד.*?(\d+)'
    match = re.search(po_box_pattern, street_name)
    if match:
        record['po_box'] = match.group(1)  # Extract the number
    return record   

def find_tree_column_index(tree, column_name):
    columns = tree["columns"]
    if column_name in columns:
        return columns.index(column_name)
    return -1  # or handle the error as appropriate


def load_file(tree, text_area):
    file_path = filedialog.askopenfilename()
    display_file_contents(file_path, tree, text_area)


def load_excel_orgin_file(tree, text_area):
   file_loaded = False
   try:
        # Read the Excel file
        file_path = filedialog.askopenfilename()
        df = pd.read_excel(file_path)

        # Clear the Treeview
        tree.delete(*tree.get_children())

        # Process each row in the DataFrame
        for index, row in df.iterrows():
            # Parse and reverse Hebrew words, then insert into the tree
            # Assuming 'parse_line' and 'util.reverse_word_if_hebrew' can handle individual cell values
            #reversed_row = [util.reverse_word_if_hebrew(word) if isinstance(word, str) else word for word in row]
           #tree.insert("", tk.END, values=reversed_row)
            
             tree.insert("", tk.END, values=row.tolist())

        file_loaded = True
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, "Found and read the file. Next step is to load the .txt file")
        

   except Exception as e:
        # Handle exceptions
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, f"Error reading file: {e}")

   return file_loaded



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
    extracted_values = []
    for field_name, start, length in util.extraction_specs:
        extracted_values.append(util.extract_mid(line, start, length))

    return extracted_values


def process_postal_codes(tree, postal_code_col):
    for item in tree.get_children():
        # Get the current value of the postal code
        postal_code = tree.item(item, 'values')[postal_code_col]

        # Check for all-zero postal codes and mark them
        if postal_code == '0000000':
            #TO DO: replace the value in the tree with '';
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


def setup_treeview(frame):
    tree = ttk.Treeview(frame)

    # Define the columns based on the extraction_specs
    column_ids = util.column_names
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



def update_with_combined_values(tree, private_col, family_col):
    for item in tree.get_children():
        row_data = list(tree.item(item, 'values'))

        private_value = row_data[private_col].strip()  # Remove leading/trailing spaces
        family_value = row_data[family_col].strip()  # Remove leading/trailing spaces

        # Combine the values
        combined_value = private_value + " " + family_value

        # Update the row with the combined value
        row_data.append(combined_value)
        tree.item(item, values=row_data)