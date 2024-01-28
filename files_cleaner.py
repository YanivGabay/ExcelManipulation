import os
from PIL import Image

def cleanfiles(folder_name,excel_file_path):
    directory = os.path.dirname(excel_file_path)
    folder_path = os.path.join(directory, folder_name)
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