 

from constants import EXTRACTION_FORMULA
import re
from src.FromMot.clean_records import process_record

def parse_text_file(file) -> list:
    text_data = []
    for line in file:
        parsed_line = parse_line(line)  
        #print(f"line before reversing {parsed_line}")
        reversed_line = [reverse_word_if_hebrew(word) for word in parsed_line]  
        column_names = [spec[0] for spec in EXTRACTION_FORMULA]
        print(f"line after reversing {reversed_line}")
        single_line_data = dict(zip(column_names, reversed_line))

        
        print(single_line_data)
        processed_record = process_record(single_line_data)  
        text_data.append(processed_record)
    return text_data

def extract_mid(text, start_position, length):
    adjusted_start = start_position - 1
    return text[adjusted_start:adjusted_start + length]

def parse_line(line):
    extracted_values = []
    for field_name, start, length in EXTRACTION_FORMULA:
        extracted_values.append(extract_mid(line, start, length))

    return extracted_values

def reverse_word_if_hebrew(word : str) -> str:
    hebrew_check = re.compile('[\u0590-\u05FF]+')
    return word[::-1] if hebrew_check.search(word) else word    