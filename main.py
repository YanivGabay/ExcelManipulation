import tkinter as tk
from tkinter import filedialog, scrolledtext
import pandas as pd
from datetime import datetime
import os
import re

def display_file_contents(file_path):
    encodings = ['utf-8', 'windows-1255', 'iso-8859-8']  # List of encodings to try
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                contents = file.read()
            print('curr encoding: ', encoding)
            reversed_contents = reverse_hebrew_words(contents)    
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, reversed_contents)
            break  # Break the loop if the file is successfully read
        except UnicodeDecodeError:
            continue  # Try the next encoding
        except Exception as e:
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, f"Error reading file: {e}")
            break


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

def reverse_hebrew_words(text):
    reversed_text = []
    for line in text.splitlines():
        words = line.split()
        reversed_line = ' '.join(word[::-1] if is_hebrew(word) else word for word in words)
        reversed_text.append(reversed_line)
    return '\n'.join(reversed_text)


# Set up the GUI
root = tk.Tk()
root.title("Text File Viewer")

load_button = tk.Button(root, text="Load File Manually", command=load_file)
load_button.pack()

auto_load_button = tk.Button(root, text="Load Today's File", command=load_file_auto)
auto_load_button.pack()

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=200, height=40)
text_area.pack(padx=10, pady=10)

root.mainloop()
