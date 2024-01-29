import os
import json
import hashlib
from datetime import datetime as dt
import datetime
import sys

universal_dir_path = None

def print_help():
    print("")
    print("Usage:")
    print("")
    print("  Maruti init                - Initialize a new Maruti repository")
    print("  Maruti add <file>          - Add a file to the index")
    print("  Maruti commit -m <message> - Commit changes with a message")
    print("  Maruti rmadd <file>        - Remove a file from the index")
    print("  Maruti rmcommit            - Remove last commit")
    print("  Maruti log                 - Display commit log")
    print("  Maruti checkout <commit>   - Checkout a specific commit")
    print("  Maruti help                - To see this usage help")
    print("  Maruti status              - To see status")
    print("  Maruti user show           - To see present user")
    print("  Maruti user set <username> - To change user")
    print("  Maruti push <path>         - To push your file to another folder")
    print((""))
    print("Created by - Swet Lakhani")
    print("")

def init_vcs(repo_path):
    if not os.path.exists(os.path.join(repo_path, ".maruti")):

        username = input("Enter your username: ")
        print("")

        vcs_dir = os.path.join(repo_path, '.maruti')
        
        branches_dir = os.path.join(vcs_dir, 'branches')
        main_branch_dir = os.path.join(branches_dir, 'main')
        objects_dir = os.path.join(vcs_dir, 'objects')
        added_json_path = os.path.join(main_branch_dir, 'added.json')
        index_json_path = os.path.join(main_branch_dir, 'index.json')
        users_txt_path = os.path.join(main_branch_dir, 'users.txt')
        
        os.makedirs(main_branch_dir, exist_ok=True)
        os.makedirs(objects_dir, exist_ok=True)

        with open(added_json_path, 'w') as added_file:
            json.dump({}, added_file)
        with open(index_json_path, 'w') as index_file:
            json.dump({}, index_file)

        timestamp = dt.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(users_txt_path, 'w') as users_file:
            users_file.write(f"{timestamp} {username}\n")

        print(f"Initialized repository at {repo_path}")
        print("")

    else :
         print("")
         print("This folder has already been intialised once...")
         print("")

def calculate_file_hash_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            md5.update(chunk)
    return md5.hexdigest()

def add_command(filename):
    
    currdir=os.getcwd()
    file_path = os.path.join(currdir, filename)

    if not os.path.exists(file_path):
        print(f"The file '{filename}' does not exist.")
        return


    file_hash = calculate_file_hash_md5(file_path)
    
    vcs_base_dir = os.path.join(currdir, '.maruti', 'branches', 'main')

    index_path = os.path.join(vcs_base_dir, 'index.json')
    added_path = os.path.join(vcs_base_dir, 'added.json')

    with open(index_path, 'r') as index_file:
        index_data = json.load(index_file)

    index_data[filename] = file_hash

    with open(index_path, 'w') as index_file:
        json.dump(index_data, index_file, indent=2)

    with open(added_path, 'r') as added_file:
        added_data = json.load(added_file)

    added_data[filename] = file_hash

    with open(added_path, 'w') as added_file:
        json.dump(added_data, added_file, indent=2)

    print(f"Added '{filename}' to the index.")

def rmadd_command():
    current_dir = universal_dir_path

    index_path = os.path.join(current_dir,'.maruti', 'branches', 'main', 'index.json')
    added_path = os.path.join(current_dir,'.maruti', 'branches', 'main', 'added.json')

    with open(added_path, 'w') as json_file:
        json.dump({}, json_file)
    
    with open(index_path, 'r') as index_file:
        index_data = json.load(index_file)

def status_command():

    current_dir = os.getcwd()

    index_path = os.path.join(current_dir,'.maruti', 'branches', 'main', 'index.json')
    added_path = os.path.join(current_dir,'.maruti', 'branches', 'main', 'added.json')

    with open(index_path, 'r') as index_file:
        index_data = json.load(index_file)

    with open(added_path, 'r') as added_file:
        added_data = json.load(added_file)

    current_files = []
    for f in os.listdir('.'):
        if os.path.isfile(f):
            current_files.append(f)

    untracked_files = [file for file in current_files if file not in added_data or calculate_file_hash_md5(file) != added_data.get(file)]

    tracked_files = [file for file in current_files if file in added_data and calculate_file_hash_md5(file) == added_data.get(file)]

    print("On branch main \n")
    if tracked_files:
        print("Changes to be committed:")
        for file in tracked_files:
            print(f"- {file}")
        print("\n")
            
    if untracked_files:
        print("Untracked files:")
        for file in untracked_files:
            print(f"- {file}")
    else:
        print("All files are tracked.")

def merge_json(source_file, destination_file):
    with open(source_file, 'r') as source_file:
        source_data = json.load(source_file)

    try:
        with open(destination_file, 'r') as destination_file:
            destination_data = json.load(destination_file)
    except FileNotFoundError:
        destination_data = {}

    destination_data.update(source_data)

    with open(destination_file, 'w') as destination_file:
        json.dump(destination_data, destination_file, indent=2)

def commit_vcs(usermsg):

    base_dir = universal_dir_path

    src_json_file = os.path.join(base_dir,'.maruti','branches','main','index.json')
    source_file = src_json_file

    src_added_file = os.path.join(base_dir,'.maruti','branches','main','added.json')
    source_added_file = src_added_file

    if os.path.getsize(source_added_file) == 2 :
        print("No Tracked Files are present. So, Unable to do commit")
        return
    
    hash_val = calculate_file_hash_md5(src_json_file)
    dstn_json_file = os.path.join(base_dir,'.maruti','objects',hash_val)
    destination_file = dstn_json_file
        
    with open(source_file, 'r') as source_file:
        source_data = json.load(source_file)

    with open(source_added_file, 'r') as source_file:
        source_added_data = json.load(source_file)
    
    try:
        with open(destination_file, 'r') as dstn_file:
            destination_data = json.load(dstn_file)
    except FileNotFoundError:
        destination_data = {}

        destination_data["all"]=source_data

        destination_data["author"]= "swet"

        destination_data["changes"]=source_added_data

        destination_data["message"]=usermsg

        destination_data["timestamp"]= datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(src_added_file, 'w') as json_file:
        json.dump({}, json_file)

    with open(destination_file, 'w') as destination_file:
        json.dump(destination_data, destination_file, indent=2)

def commit(usermsg):

    currdir=universal_dir_path
    fpath=f"{currdir}/.maruti/branches/main/added.json"
 
    file_hash=calculate_file_hash_md5(fpath)
    objectPath = f"{currdir}/.maruti/objects"

    cfiles=os.listdir(objectPath)

    match="0"
    last=""

    add_data={}
    with open(f"{fpath}", 'r') as file:
        add_data = json.load(file)

    if not cfiles:
        temp_data={}
        temp_data["changes"]=add_data
        temp_data["all"]=add_data
        temp_data["message"]=usermsg

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        temp_data["timestamp"]=timestamp

        new_file_path = f"{objectPath}/{file_hash}.json" 
        json_data = json.dumps(temp_data, indent=4)

        with open(new_file_path, 'w') as json_file:
         json_file.write(json_data)

        # empty_dict={}
        # json_data = json.dumps(empty_dict)

        with open(fpath, 'w') as file:
          file.write("")
    
        # with open(fpath, 'w') as json_file:
        #     json_file.write(json_data)

        print("Done successfully")
        
        return 


    for file in cfiles: 
         creation_time = os.path.getctime(f"{objectPath}/{file}")
         creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
         if(creation_time_readable>match):
            match=creation_time_readable
            last=file
    
    last_data={}
    with open(f"{objectPath}/{last}", 'r') as file:
        last_data = json.load(file)

   

    new_data = {
    "changes": add_data
    } 
    
    for key in new_data["changes"]:
        last_data["all"][key]=new_data["changes"][key]
    
    last_data["changes"]=new_data["changes"]
    last_data["message"]=usermsg

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    last_data["timestamp"]=timestamp

    new_file_path = f"{objectPath}/{file_hash}.json" 
    json_data = json.dumps(last_data, indent=4)

    with open(new_file_path, 'w') as json_file:
      json_file.write(json_data)

    with open(fpath, 'w') as file:
           file.write("")

    print("Done successfully")

def read_usernames():

    base_dir = os.getcwd()
    file_path = os.path.join(base_dir,'.maruti','branches','main','users.txt')

    # usernames = []

    # try:
    #     with open(file_path, 'r') as file:
    #         # Read lines from the file and remove leading/trailing whitespaces
    #         usernames = [line.strip() for line in file.readlines()]
    # except FileNotFoundError:
    #     print(f"Error: File '{file_path}' not found.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")

    # print(usernames[0][20:])


    try:
        with open(file_path, 'r') as file:
            line = file.readline()
            components = line.split()
            username = f"{components[2:]}"
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    for file in components:
        print(file)
    print(username)

def main():
    
    global universal_dir_path

    print("")
    print("VCS - Version Control System")
    print("System Programming")

    
    while True :

        print("")
        print("Press - 1 : TO PROCEED FURTHER")
        print("Press - 2 : TO EXIT")
        print("")

        ip = input("Enter : ")

        if ip == "1":
            if universal_dir_path == None:
                universal_dir_path = input("Enter directory location where you want to make .maruti repository / .maruti repository exists : ")
                print()
        
            if os.path.isdir(universal_dir_path) == False :
                print("The path you have given doesn't exists, kindly give path which exists")
                print()
                universal_dir_path = None
                continue
            
            break
        elif ip == "2":
            exit()
        else :   
            print("Enter valid input!!!")
            
    while True:
        
        user_input = input("Enter a command (type 'help' for usage): ").split()
        command = user_input[0]

        if command == 'help':
            print_help()
        elif command == 'init':
            init_vcs(universal_dir_path)
        elif command == 'add':
            if len(user_input) > 1:
                file_name = user_input[1]
                add_command(file_name)
            else:
                print("Error: Specify a file to add.")
        elif command == 'status':
            status_command()
        elif command == 'commit':
            if len(user_input) > 2:
                if(user_input[1]=='-m'):
                    user_msg = " ".join(user_input[2:])
                    # commit_vcs(user_msg)
                    commit(user_msg)
                else :
                    print("Error: Enter valid format to do commit")
            else :
                print("Error: Specify a message to add.")
        elif command == 'rmadd':
            rmadd_command()   
        elif command == 'get':
            read_usernames()
        elif command == 'exit':
            break
        else:
            print(f"Error: Unknown command '{command}'. Type 'help' for usage.")

if __name__ == "__main__":
    
    main()
    

