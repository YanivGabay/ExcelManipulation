import tkinter as tk
from tkinter import ttk
import gui_components as gui_comp
import file_processing as file_proc
import utilities as util
import export as export_service
from tkinter import PhotoImage
import options_menu as options_menu

def main():
    root = tk.Tk()
    root.title("Text File Viewer")
    root.geometry('800x600')
    root.maxsize(1200, 800)
    if  root.tk.call('tk', 'windowingsystem')=='win32':
        root.iconbitmap('Resources/small.ico')  # Use .ico file for Windows
    else:
        img = PhotoImage(file='Resources/third_icon.png')  # Use .png or .gif file for other OS
        root.tk.call('wm', 'iconphoto', root._w, img)
    menu = tk.Menu(root)
    
    options_menu.create_options_menu(menu, root)

    root.config(menu=menu)
    
    main_frame = ttk.Frame(root)
    main_frame.pack(fill='both', expand=True)
    
      
    # Create bottom frame first to get the tree reference
    bottom_frame, tree = gui_comp.create_bottom_frame(main_frame)
    bottom_frame.pack(fill='both', expand=True)
    
    # Now create top frame with lambda functions for load_file and load_file_auto
    top_frame, text_area = gui_comp.create_top_frame(main_frame, lambda: file_proc.load_file(tree,text_area),
                                                   lambda: file_proc.load_excel_orgin_file(tree,text_area),
                                                      lambda: export_service.save_to_excel(tree, "ExportData.xlsx",text_area))
    top_frame.pack(side='top', fill='x')

    root.mainloop()

if __name__ == "__main__":
    main()
