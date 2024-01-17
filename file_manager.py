import os
import hashlib
import json
import sys

def calculate_md5(file_path):
    
    md5_hash = hashlib.md5()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()

def get_file_info(file_path):

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    md5_hash = calculate_md5(file_path)

    return {
        "Filename": file_name,
        "File size": file_size,
        "MD5 hash": md5_hash
    }

def process_directory(directory_path):

    file_info_dict = {}

    for file_name in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, file_name)):
            file_path = os.path.join(directory_path, file_name)
            file_info = get_file_info(file_path)
            file_info_dict[file_name] = file_info

    json_file_path = "file_info.json"
    with open(json_file_path, "w") as json_file:
        json.dump(file_info_dict, json_file, indent=4)

    print(f"File information has been saved to {json_file_path}")

directory_path = input("Enter the directory path: ")

if not os.path.exists(directory_path):
    print(f"Directory '{directory_path}' not found.")
else:
    process_directory(directory_path)
