import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from src.ToMot.load_to_mot import load_to_mot
from src.FromMot.load_from_mot import load_from_mot


# Set up the main application window
root = tk.Tk()
root.title("Ministry File Handler")
root.geometry("400x200")  # Set the size of the window

# Add buttons
to_mot_button = ttk.Button(root, text="TO MOT / למשרד התחבורה", command=load_to_mot)
to_mot_button.pack(expand=True)

from_mot_button = ttk.Button(root, text="FROM MOT / ממשרד התחבורה", command=lambda: load_from_mot(root))
from_mot_button.pack(expand=True)


# Start the GUI event loop
root.mainloop()
