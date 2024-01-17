import os
import hashlib
import json
import sys
import shutil

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
        "MD5 hash": md5_hash,
        "File_path": file_path
    }

def process_directory(directory_path):

    file_info_dict = {}

    for file_name in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, file_name)):
            file_path = os.path.join(directory_path, file_name)
            file_info = get_file_info(file_path)
            file_info_dict[file_name] = file_info

    fil_nam = "file_info.json"
    json_file_path = os.path.join(directory_path, fil_nam)
    
    with open(json_file_path, "w") as json_file:
        json.dump(file_info_dict, json_file, indent=4)

def copy_to_particular_directory(src_drt,dstn_drt):        

    files_to_copy = []

    for entry in os.listdir(src_drt):
        entry_path = os.path.join(src_drt, entry)
        if os.path.isfile(entry_path):
            files_to_copy.append(entry)
    
    for file_name in files_to_copy:
        source_file_path = os.path.join(src_drt, file_name)
        destination_file_path = os.path.join(dstn_drt, file_name)
        shutil.copy2(source_file_path, destination_file_path)
        print(f"File '{file_name}' copied to '{dstn_drt}'.")

    process_directory(dstn_drt)
    

src_drt = input("Enter src Directory : ")
if(not os.path.exists(src_drt)):
        print("Source Directory don't exist")
        sys.exit()
    
dstn_drt = input("Enter dstn Directory : ")
if(not os.path.exists(dstn_drt)):
        print("Destination Directory don't exist")
        sys.exit()

copy_to_particular_directory(src_drt,dstn_drt)
