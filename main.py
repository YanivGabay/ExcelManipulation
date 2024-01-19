import tkinter as tk
from tkinter import ttk
import gui_components as gui_comp
import file_processing as file_proc
import utilities as util

#to ask gal:
#about כתובת נהג תא דואר


def main():
    root = tk.Tk()
    root.title("Text File Viewer")
    root.geometry('800x600')
    root.maxsize(1200, 800)

    main_frame = ttk.Frame(root)
    main_frame.pack(fill='both', expand=True)
    
      
    # Create bottom frame first to get the tree reference
    bottom_frame, tree = gui_comp.create_bottom_frame(main_frame, util.extraction_specs)
    bottom_frame.pack(fill='both', expand=True)
    
    # Now create top frame with lambda functions for load_file and load_file_auto
    top_frame, text_area = gui_comp.create_top_frame(main_frame, lambda: file_proc.load_file(tree,text_area),
                                                      lambda: file_proc.load_file_auto(tree),
                                                      lambda: file_proc.save_to_excel(tree, "ExportData.xlsx",text_area))
    top_frame.pack(side='top', fill='x')

    root.mainloop()

if __name__ == "__main__":
    main()
