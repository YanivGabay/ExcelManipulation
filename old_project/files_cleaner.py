import os
from PIL import Image
import zipfile


def print_contents_of_directory(directory_path):
    print(f"Contents of '{directory_path}':")
    for root, dirs, files in os.walk(directory_path):
        for name in files:
            print(os.path.join(root, name))
        for name in dirs:
            print(os.path.join(root, name))

def cleanfiles(folder_name,excel_file_path,zip_mode):
    directory = os.path.dirname(excel_file_path)
    
    if zip_mode:
        zip_path = os.path.join(directory, f"{folder_name}.zip")
        if zipfile.is_zipfile(zip_path):
            extract_path = os.path.join(directory, folder_name)  # Specify a unique extract path for each ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
                print(f"Extracted ZIP: {zip_path}")
            
            zip_file_name = os.path.splitext(os.path.basename(zip_path))[0]  # Get the name of the ZIP file without the extension
            print_contents_of_directory(extract_path)  # Print contents after extraction
            deleteFiles(extract_path, zip_file_name)
   
def deleteFiles(folder_path,zip_file_name):
    print(f"Cleaning folder: {folder_path}")
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # Delete specific images
            if file in ['קישור לסרטון העבירה.jpg', 'מספר לוחית רישוי.jpg']:
                os.remove(file_path)
                print(f"Deleted: {file_path}")

            # Rename and convert the third image to PNG
            if file == 'רגע העבירה.jpg':
                img = Image.open(file_path)
                new_file_name = f"{zip_file_name}_moment.png"  # Use the ZIP file name for the new image name
                new_file_path = os.path.join(root, new_file_name)
                img.save(new_file_path, 'PNG')
                os.remove(file_path)
                print(f"Converted and renamed: {new_file_path}")