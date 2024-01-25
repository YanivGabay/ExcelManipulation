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
                
                text_area.delete('1.0', tk.END)
                text_area.insert(tk.END, "Found and read the Text file.")


                text_data = process_txt_file(text_data, text_area)
                transfer_data_to_tree(tree,text_data,text_area)
                file_loaded = True          
               # text_area.delete('1.0', tk.END)
               # text_area.insert(tk.END, "File loaded successfully. (:")
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
    
def transfer_data_to_tree(tree,text_data,text_area):
   # print("Number of rows in the tree:", len(tree.get_children()))
    try:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, "Transfering data to the tree")
        for child in tree.get_children():
            #print("Processing tree child")  
            tree_item = tree.item(child)
            tree_address = tree_item['values'][find_tree_column_index(tree, 'Identifier')]
            #print("Tree Address:", tree_address)  # Debug print
            tree_adress_str = str(tree_address).strip()
            for record in text_data:
                 #print("Record Address:", record['costumer_code'])  # Debug print
                  if record['costumer_code'] == tree_adress_str:
                     #print("Found matching record"+record['costumer_code']+tree_adress_str)
                        # Update necessary cells in the tree with data from record
                     update_tree_item(tree, child, record)
                     
                     
        highlight_rows(tree)           
    except Exception as e:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, f"Error inside transfer_data_to_tree(): {e}")


#def new_owner(row_data):
    #ownership_date = row_data["Ownership Date"]
    #report_date = row_data["Reporting Date"]


def bad_postal_code(value):
    return value == '4664000'

def highlight_rows(tree):
    print("Highlighting rows")
   
    for child in tree.get_children():
        row_data = tree.item(child, 'values')
       
       
        if bad_postal_code(row_data[find_tree_column_index(tree, "Driver's Address-Zip Code")]):
           print("Found bad postal code")
           tree.item(child, tags=('highlight',))
       # if new_owner(row_data,tree):
         #  tree.item(child, tags=('bad',))
    # Applying the highlight style to tagged items
    tree.tag_configure('highlight', background='lightblue')
    tree.tag_configure('bad', background='red')



def update_tree_item(tree, item, record):
    
    current_values = list(tree.item(item, 'values'))
   
    #print("Length of current_values:", len(current_values))
   
    current_date = datetime.now().strftime("%d-%m-%Y")
    current_values[find_tree_column_index(tree,"Approval Date")] = current_date
    
    current_values[find_tree_column_index(tree,"Number of Violations")] = '1'
   # print(temp_column_index)
    for tree_column, record_field in util.column_to_field_mapping.items():
        if tree_column in tree['columns']:
         #   print("tree_column:",tree_column)
           # print("record_field:",record_field)
            
            column_index = tree['columns'].index(tree_column)
            current_values[column_index] = record.get(record_field, '')
            
          #  print("Column Index:", column_index)
   # current_values[find_tree_column_index['Number of Violations']] = #'1'
    #
   # current_values[find_tree_column_index['Approval Date']] = #current_date


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
def process_record(record,text_area):

   try:
    record = process_postal_codes(record)

  
    record = process_full_name(record)

  
    record = process_street_name(record)
    #print(record)
    return record
   except Exception as e:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, f"Error inside Process_record(): {e}")

   

def process_txt_file(text_data, text_area): 
   
    try:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, "Cleaning the data")
        for record in text_data:
             #print("Processing record")
             if isinstance(record, dict):  # Ensure record is a dictionary
                  record = process_record(record, text_area)
             else:
                  text_area.insert(tk.END, "Error: Record is not a dictionary.\n")
                 

    except Exception as e:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, f"Error process_txt_file: {e}")

    return text_data 
def process_postal_codes(record):

       
        postal_code = record["postal_code"]
        #print("before if statem postal_code:",postal_code)
        if postal_code == '0000000':
            record["postal_code"] = 'zeros'
            
            
            
        else:
            # Process non-zero postal codes
            # Assuming 7-digit postal code
            #print("old postal_code:",postal_code)
            postal_code = postal_code[2:] + postal_code[:2]
            record["postal_code"] = postal_code
           # print("new postal_code:",postal_code)
        return record      
  
def process_full_name(record): 
    first_name = record.get('private', '').strip()
    last_name = record.get('family', '').strip()
    record['full_name'] = f"{first_name} {last_name}"
    return record
    
    #future check for insertiong into bad records
    

   
def process_street_name(record):
    
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
        df = pd.read_excel(file_path,dtype=str)

        

        df = df.replace(pd.NA, '')
        # Remove the '_x0000_' string from the column names
        #maybe more robust check in the future
        df.replace(to_replace='_x0000_', value='', regex=True, inplace=True)
        num_tree_columns = len(tree['columns'])
        # Clear the Treeview
        tree.delete(*tree.get_children())

         # Process each row in the DataFrame
        for index, row in df.iterrows():
            row_values = row.tolist()

            # Adjust the row length to match the treeview columns
            adjusted_row_values = row_values + [''] * (num_tree_columns - len(row_values))

            # Insert the adjusted row into the Treeview
            tree.insert("", tk.END, values=adjusted_row_values)

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

    # Define the columns based on the column_names
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
    #debug
   # number_of_columns = len(tree['columns'])
   # print("Number of columns in the treeview:", number_of_columns)
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