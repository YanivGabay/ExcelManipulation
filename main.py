import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from src.ToMot.load_to_mot import load_to_mot


def load_from_mot():
    print("Load FROM MOT flow")

# Set up the main application window
root = tk.Tk()
root.title("Ministry File Handler")
root.geometry("400x200")  # Set the size of the window

# Add buttons
to_mot_button = ttk.Button(root, text="TO MOT / למשרד התחבורה", command=load_to_mot)
to_mot_button.pack(expand=True)

from_mot_button = ttk.Button(root, text="FROM MOT / ממשרד התחבורה", command=load_from_mot)
from_mot_button.pack(expand=True)

# Start the GUI event loop
root.mainloop()
