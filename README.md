
# Ministry Handler Program

## About

The Ministry Handler Program is developed by me (Yaniv Gabay) for **שומרי הדרך** [Shomrei HaDerech](https://www.shomriderech.org.il/), a non-profit group working with the Driving Ministry in Israel.
This application is designed to help the office staff to process text file into excel file and vice versa.
The text files and excel files contain personal drivers information, due to the sensitivity of the data, the specific files are not shared in this repository.

## Features
![image](https://github.com/user-attachments/assets/abf97a97-be3e-4117-abb9-dbbeeb3fbe91)


- Load an excel file with the drivers information.
- Create a text file processed from that previous excel file, with the specific format needed.
- The staff should receive an text file as response from the driving ministry, and the program will process it into an excel file.
- Processed the new excel file, clean , extract zip files and create a new excel file with the staff wanted information.
- User-friendly GUI for easy interaction.
![image](https://github.com/user-attachments/assets/3d795c82-12d2-4eb1-9181-f9a3be596a73)




## Installation

The program can be run as a standalone executable or directly from the Python script. Below are the steps for both methods:

### Running the Executable

1. Download the latest version of the executable from the Releases section.
2. Double-click on the executable to start the program.

### Running from Source

1. Ensure that Python 3.x is installed on your machine.
2. Clone this repository or download the source code.
3. Create dedicated virtual environment:

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

   - Windows: `venv\Scripts\Activate.ps`
   - Linux/Mac: `source venv/bin/activate`

   i needed to add to the activate file the following line:
   ```bash
   $Env:TCL_LIBRARY="C:\Users\Yaniv\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
   ``` 
   had problem with the tkinter library.
   
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the program:

   ```bash
   python main.py
   ```

### Building the Executable

To generate a `.exe` file for easier distribution and use, follow these steps:

1. Navigate to the project directory.
2. Use PyInstaller with the following command:
   
   ```bash
   pyinstaller --onefile --windowed main.py
   ```

## Usage

To use the program:

1. Start the program via the executable or the Python script.
2. Follow the on-screen instructions to load files and perform data operations.

d parties. Redistribution or commercial use is not permitted without explicit permission.

## Contact

For more information or assistance, please contact me at [yaniv242@gmail.com](yaniv242@gmail.com).

