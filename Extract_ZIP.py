import os
import zipfile

# Specify the path to the folder containing the zip files
zip_folder = r'SHP_FILES'

# Iterate over each file in the folder
for file_name in os.listdir(zip_folder):
    file_path = os.path.join(zip_folder, file_name)
    if os.path.isfile(file_path) and file_name.endswith('.zip'):
        # Extract the zip file into a folder with the same name
        folder_name = os.path.splitext(file_name)[0]
        folder_path = os.path.join(zip_folder, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(folder_path)

        # Delete the zip file
        os.remove(file_path)
