

import re
import tkinter as tk
from datetime import datetime

def process_record(record):


    record = process_postal_codes(record)

  
    record = process_full_name(record)

  
    record = process_street_name(record)

    record = clean_record_fields(record)
    #print(record)
    return record


def process_postal_codes(record):

    postal_code = record["postal_code"]
  
    if postal_code == '0000000':
        record["postal_code"] = '00000'

    else:
        # Process non-zero postal codes
        # Assuming 7-digit postal code
        #print("old postal_code:",postal_code)
        postal_code = postal_code[2:] + postal_code[:2]
        record["postal_code"] = postal_code
        print("new postal_code:",postal_code)
    return record      
  
def process_full_name(record): 
    first_name = record.get('private', '').strip()
    last_name = record.get('family', '').strip()
    record['full_name'] = f"{first_name} {last_name}"
    return record
    
    #future check for insertiong into bad records
    
def clean_record_fields(record):
    # Iterate over each field in the record
    for key, value in record.items():
        # Strip leading and trailing spaces and preserve internal spaces between words
        if isinstance(value, str):
            record[key] = ' '.join(value.split())
    return record
   
def process_street_name(record):
    
    street_name = record.get('street_name', '').strip()
    # Regex pattern to match 'תד', 'ת.ד', or 'ת"ד', followed by numbers
    po_box_pattern = r'ת.*ד.*?(\d+)'
    match = re.search(po_box_pattern, street_name)
    if match:
        record['po_box'] = match.group(1)  # Extract the number
    return record   

