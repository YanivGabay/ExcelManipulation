import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from src.ToMot.file_handling import read_excel_file, create_text_content, save_text_file
from datetime import datetime



def load_to_mot():
    file_path = filedialog.askopenfilename(title="Select the Excel file",
                                           filetypes=[("Excel files", "*.xls"), ("Excel files", "*.xlsx")])
    if not file_path:
        messagebox.showinfo("Info", "No file selected!")
        return
    
    try:
        # Read the Excel file
        df = read_excel_file(file_path)
        # Create the text content
        content = create_text_content(df)
        # Get the file name
        file_name = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")],
                                                 initialfile=f"to_mot_{datetime.now().strftime('%Y%m%d')}.txt")
        if file_name:
            save_text_file(content, file_name)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

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
