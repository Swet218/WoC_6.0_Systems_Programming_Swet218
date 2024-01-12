import os
import shutil

# def traverse_directory(directory):
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             file_path = os.path.join(root, file)
#             print(file_path)

def organize_files(directory):
  
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            _, file_extension = os.path.splitext(filename)
            file_extension = file_extension.lower()  # Convert to lowercase for consistency

            extension_folder = os.path.join(directory, file_extension[1:])
            if not os.path.exists(extension_folder):
                os.makedirs(extension_folder)

            shutil.move(file_path, os.path.join(extension_folder, filename))
            print(f"Moved '{filename}' to '{extension_folder}'.")


directory_path = input("Enter the directory path: ")

if not os.path.isdir(directory_path):
    print(f"The path '{directory_path}' is not a directory.")
else:
    print("Current Directory:", directory_path)
    print("Below are the files present in Current Directory")
    #traverse_directory(directory_path)
    organize_files(directory_path)
    

