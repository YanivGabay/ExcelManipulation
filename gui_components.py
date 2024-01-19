import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import file_processing as fp

def create_top_frame(parent, load_file_func, load_file_auto_func):
    top_frame = ttk.Frame(parent)
    load_button = tk.Button(top_frame, text="Load File Manually", command=load_file_func)
    load_button.pack(side='left', padx=10, pady=10)
    auto_load_button = tk.Button(top_frame, text="Load Today's File", command=load_file_auto_func)
    auto_load_button.pack(side='left', padx=10)
    text_area = scrolledtext.ScrolledText(top_frame, wrap=tk.WORD, width=80, height=5)
    text_area.pack(side='left', fill='x', expand=True, padx=10, pady=10)
    return top_frame , text_area

def create_bottom_frame(parent, extraction_specs):
    
    bottom_frame = ttk.Frame(parent)
    tree = fp.setup_treeview(bottom_frame, extraction_specs)
   
    y_scroll = ttk.Scrollbar(bottom_frame, orient="vertical", command=tree.yview)
    y_scroll.pack(side='right', fill='y')
    tree.configure(yscrollcommand=y_scroll.set)
    x_scroll = ttk.Scrollbar(bottom_frame, orient="horizontal", command=tree.xview)
    x_scroll.pack(side='bottom', fill='x')
    tree.configure(xscrollcommand=x_scroll.set)
    tree.pack(side='left', fill='both', expand=True)



    return bottom_frame , tree





