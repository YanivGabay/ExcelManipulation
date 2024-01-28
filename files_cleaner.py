import os
from PIL import Image
import zipfile

def cleanfiles(folder_name,excel_file_path,zip_mode):
    directory = os.path.dirname(excel_file_path)
    folder_path = os.path.join(directory, folder_name)
    #if zip mode
    #we will decompress the files
    #and clean
    if(zip_mode):
        new_path = f"{folder_path}.zip"
        folder_path = directory 
        #we extract all the files in
        #the excel directory
        if zipfile.is_zipfile(new_path):
            with zipfile.ZipFile(new_path, 'r') as zip_ref:
            # Extract all the contents into the directory
             zip_ref.extractall(directory)
        print(new_path)
    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            # Delete two specific images
            if file in ['קישור לסרטון העבירה.jpg', 'מספר לוחית רישוי.jpg']:
                os.remove(file_path)


             # Rename and convert the third image to PNG
            if file == 'רגע העבירה.jpg':
                img = Image.open(file_path)
                new_file_path = os.path.join(folder_path, 'image3.png')
                img.save(new_file_path, 'PNG')
                os.remove(file_path)  
