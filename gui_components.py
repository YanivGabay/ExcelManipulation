import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import file_processing as fp

def create_top_frame(parent, load_file_func, load_excel_orgin_file_func,save_excel_func):
    top_frame = ttk.Frame(parent)
    load_button = tk.Button(top_frame, text="Load Txt File Manually", command=load_file_func)
    load_button.pack(side='left', padx=10, pady=10)

    excel_load_file = tk.Button(top_frame, text="Load Excel File", command=load_excel_orgin_file_func)
    excel_load_file.pack(side='left', padx=10)

    save_excel_button = tk.Button(top_frame, text="Save to Excel", command=save_excel_func)
    save_excel_button.pack(side='left', padx=10, pady=10)

    text_area = scrolledtext.ScrolledText(top_frame, wrap=tk.WORD, width=80, height=5)
    text_area.pack(side='left', fill='x', expand=True, padx=10, pady=10)
    return top_frame , text_area

def create_bottom_frame(parent):
    
    bottom_frame = ttk.Frame(parent)
    tree = fp.setup_treeview(bottom_frame)
   
    y_scroll = ttk.Scrollbar(bottom_frame, orient="vertical", command=tree.yview)
    y_scroll.pack(side='right', fill='y')
    tree.configure(yscrollcommand=y_scroll.set)
    x_scroll = ttk.Scrollbar(bottom_frame, orient="horizontal", command=tree.xview)
    x_scroll.pack(side='bottom', fill='x')
    tree.configure(xscrollcommand=x_scroll.set)
    tree.pack(side='left', fill='both', expand=True)



    return bottom_frame , tree






