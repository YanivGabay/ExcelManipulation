import tkinter as tk

def create_options_menu(menu, root):
    #submenu 
    file_menu = tk.Menu(menu, tearoff=False)
    file_menu.add_command(label="Exit", command=root.destroy)
    file_menu.add_command(label="Reset", )
    menu.add_cascade(label="File", menu=file_menu)
    # submenu
    option_menu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(label="Options", menu=option_menu)
    
    colors_menu = tk.Menu(option_menu, tearoff=False)
    option_menu.add_cascade(label="Colors", menu=colors_menu)
    colors_menu.add_command(label="Light-Red", command=lambda: print("Red"))
    colors_menu.add_command(label="Green-Brown", command=lambda: print("Green"))
    colors_menu.add_command(label="Deep-Blue", command=lambda: print("Blue"))
