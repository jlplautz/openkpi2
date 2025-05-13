import zipfile
import os

# Path to the ZIP file
zip_file_path = r"C:\Userdata\proj2025\openkpi2\pm"

# Directory where the files will be extracted
extract_to_directory = r"C:\Userdata\proj2025\openkpi2\pm\extrated_files"

# Ensure the target directory exists
os.makedirs(extract_to_directory, exist_ok=True)

# Iterate through all files in the zip_file_path directory
for file_name in os.listdir(zip_file_path):
    # Check if the file has a .zip extension
    if file_name.endswith(".zip"):
        zip_file_full_path = os.path.join(zip_file_path, file_name)
        
        # Unzip the file
        with zipfile.ZipFile(zip_file_full_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_directory)
        
        print(f"Extracted: {file_name} to {extract_to_directory}")

print("All ZIP files have been extracted.")