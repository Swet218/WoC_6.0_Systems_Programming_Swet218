import os
import json
import hashlib
from datetime import datetime as dt
import datetime
import sys
import base64

universal_dir_path = None


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def calculate_file_hash_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            md5.update(chunk)
    return md5.hexdigest()

def encode_file_content_to_base64(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
        return base64.b64encode(binary_data).decode('utf-8')


def help():
    print("")
    print("Usage:")
    print("")
    print("  Maruti init                - Initialize a new Maruti repository")
    print("  Maruti add <file>          - Add a file to the index")
    print("  Maruti commit -m <message> - Commit changes with a message")
    print("  Maruti rmadd               - Remove all files from the index")
    print("  Maruti rmcommit            - Remove last commit")
    print("  Maruti log                 - Display commit log")
    print("  Maruti checkout <commit>   - Checkout a specific commit")
    print("  Maruti help                - To see this usage help")
    print("  Maruti status              - To see status")
    print("  Maruti user show           - To see present user")
    print("  Maruti user set <username> - To change user")
    print("  Maruti push <path>         - To push your file to another folder")
    print("  Maruti clear/cls           - To clear Terminal Screen")
    print("")
    print("Created by - Swet Lakhani")
    print("")

def init(repo_path):
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

        timestamp = dt.now()

        with open(users_txt_path, 'w') as users_file:
            users_file.write(f"Date: {timestamp.strftime('%d-%m-%Y')}\n")
            users_file.write(f"Timestamp: {timestamp.strftime('%H:%M:%S')}\n")
            users_file.write(f"User: {username}\n")

        print(f"Initialized repository at {repo_path}")
        print("")

    else :
         print("")
         print("This folder has already been intialised once...")
         print("")

def add_command(filename):
    
    file_path = os.path.join(universal_dir_path, filename)

    if not os.path.exists(file_path):
        print(f"The file '{filename}' does not exist.")
        return


    file_hash = calculate_file_hash_md5(file_path)
    
    vcs_base_dir = os.path.join(universal_dir_path, '.maruti', 'branches', 'main')

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

    index_path = os.path.join(universal_dir_path,'.maruti', 'branches', 'main', 'index.json')
    added_path = os.path.join(universal_dir_path,'.maruti', 'branches', 'main', 'added.json')

    if os.path.getsize(added_path) == 2:

        print("You dont't have any tracked files")
        print("Please add track files to continue")
        return

    with open(index_path, 'r') as index_file:
        index_data = json.load(index_file)

    with open(added_path, 'r') as added_file:
        added_data = json.load(added_file)


    with open(added_path, 'w') as json_file:
        json.dump({}, json_file)

    for f in added_data:
        if f in index_data:
            del index_data[f]

    with open(index_path, 'w') as index_file:
        json.dump(index_data, index_file,indent=2)

def status_command():

    index_path = os.path.join(universal_dir_path,'.maruti', 'branches', 'main', 'index.json')
    added_path = os.path.join(universal_dir_path,'.maruti', 'branches', 'main', 'added.json')

    with open(index_path, 'r') as index_file:
        index_data = json.load(index_file)

    with open(added_path, 'r') as added_file:
        added_data = json.load(added_file)

    current_files = []
    for f in os.listdir(universal_dir_path):
        file_path = os.path.join(universal_dir_path, f)
        if os.path.isfile(file_path):
            current_files.append(f)

    if current_files == [] :
        print("There are no files present.")
        print("Please Enter Files to track")
        return

    untracked_files = [file for file in current_files if file not in index_data or calculate_file_hash_md5(os.path.join(universal_dir_path,file)) != index_data.get(file)]

    tracked_files = [file for file in current_files if file in added_data and calculate_file_hash_md5(os.path.join(universal_dir_path,file)) == added_data.get(file)]

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
 
def commit(usermsg):

    fpath=os.path.join(universal_dir_path,'.maruti','branches','main','added.json')

    if os.path.getsize(fpath) == 2:
        print("Please add files to track and the commit")
        return
 
    file_hash=calculate_file_hash_md5(fpath)
    objectPath=os.path.join(universal_dir_path,'.maruti','objects')

    cfiles=os.listdir(objectPath)

    match="0"
    last=""

    add_data={}
    with open(f"{fpath}", 'r') as file:
        add_data = json.load(file)
   
    if not cfiles:
        temp_data={}

        new_data={}
    
        for file in add_data:
            temp_path = os.path.join(universal_dir_path,file)
            encoded_data=encode_file_content_to_base64(temp_path)
            new_data[file]=encoded_data

        temp_data["changes"]=new_data
        temp_data["all"]=new_data
        temp_data["message"]=usermsg

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        temp_data["timestamp"]=timestamp

        new_file_path = f"{objectPath}/{file_hash}.json" 
        json_data = json.dumps(temp_data, indent=4)

        with open(new_file_path, 'w') as json_file:
         json_file.write(json_data)

        data = {} 
        with open(fpath, 'w') as file:
            json.dump(data, file)

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

    new_data={}
    
    for file in add_data:
            temp_path= os.path.join(universal_dir_path,file)
            encoded_data=encode_file_content_to_base64(temp_path)
            new_data[file]=encoded_data

    temp_data={}
    temp_data["changes"]=new_data

    for key in temp_data["changes"]:
        last_data["all"][key]=temp_data["changes"][key]
    
    last_data["changes"]=temp_data["changes"]
    last_data["message"]=usermsg

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    last_data["timestamp"]=timestamp

    new_file_path = f"{objectPath}/{file_hash}.json" 
    json_data = json.dumps(last_data, indent=4)

    with open(new_file_path, 'w') as json_file:
      json_file.write(json_data)

    data = {} 
    with open(fpath, 'w') as file:
        json.dump(data, file)

    print("Done successfully")

flag = 0
def rmcommit():
    global flag

    match="0"
    last=""
    objectPath=os.path.join(universal_dir_path,'.maruti','objects')
    cfiles=os.listdir(objectPath)

    cnt=0
    for f in os.listdir(objectPath):
        if cnt>1:
            break
        cnt=cnt+1

    if cnt==0:
        print("You don't have any commit to remove.")
        return 
    
    if cnt<=1:
        if flag == 0:
            print("Warning : You have only commit left.")
            print("If you try to remove once again, then it will get permanently deleted.")
            flag=1
            return

    for file in cfiles: 
         creation_time = os.path.getctime(f"{objectPath}/{file}")
         creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
         if(creation_time_readable>match):
            match=creation_time_readable
            last=file

    os.remove(f"{objectPath}/{last}")

    if cnt<=1:
        return 

    match="0"
    last=""
    cfiles=os.listdir(objectPath)

    for file in cfiles: 
         creation_time = os.path.getctime(f"{objectPath}/{file}")
         creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
         if(creation_time_readable>match):
            match=creation_time_readable
            last=file

    last_commit_path=f"{objectPath}/{last}"
    state={}

    with open(f"{last_commit_path}", 'r') as file:
        state = json.load(file)
    
    all={}
    all=state["all"]

    all_file=os.listdir(universal_dir_path)

    for file in all_file:
          if(file=="main.py"):continue
          destination_path=os.path.join(universal_dir_path,file)
          if(os.path.isfile(os.path.join(universal_dir_path,file))):
              if file in all.keys():
                  decodedContent=base64.b64decode(all[file])

                  with open(destination_path, 'wb') as file:
                        file.write(decodedContent)
              else :
                os.remove(destination_path)
  
    print("Done Successfully")

def get_username():

    usersfile_path = os.path.join(universal_dir_path,'.maruti','branches','main','users.txt')

    if not os.path.exists(usersfile_path):
        print("Warning : .maruti repository does not exist. first create it.")
        return

    username = None

    with open(usersfile_path, 'r') as file:
        for line in file:
            if line.startswith("User:"):
                username = line.split(":")[1].strip()

    print(f"Username : {username}")

def change_username(new_username):

    usersfile_path = os.path.join(universal_dir_path,".maruti","branches","main","users.txt")


    with open(usersfile_path, "r") as file:
        lines = file.readlines()

    with open(usersfile_path, "w") as file:
        for line in lines:
            if line.startswith("User:"):
                file.write(f"User: {new_username}\n")
            else:
                file.write(line)
    print("Username changed Successfully")

def log():

    log={}
    objectPath=os.path.join(universal_dir_path,'.maruti','objects')
    cfiles=os.listdir(objectPath)

    for file in cfiles: 
         creation_time = os.path.getctime(f"{objectPath}/{file}")
         creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
         log[creation_time_readable]=file
        
    myKeys = list(log.keys())
    myKeys.sort()

    usersfile_path = os.path.join(universal_dir_path,'.maruti','branches','main','users.txt')

    username = None

    with open(usersfile_path, 'r') as file:
        for line in file:
            if line.startswith("User:"):
                username = line.split(":")[1].strip()

    for x in log:
        fileName=log[x]
        filePath=f"{objectPath}/{fileName}"
        with open(f"{filePath}", 'r') as file:
         tempD = json.load(file)
        
        print(f"Author: {username}\n")
        print(f"Commit: {fileName[:-5]}\n")

        print("All files\n")

        for y in tempD["all"]:
            print(f"    {y}:{tempD["all"][y]}\n")

        print("Modified files\n")

        for y in tempD["changes"]:
            print(f"    {y} : {tempD["changes"][y]}\n")
    
        print(f"Message:{tempD["message"]}\n")
        print(f"Time Stamp:{tempD["timestamp"]}\n\n\n")

def push(dstn_path):
    
    if not os.path.isdir(dstn_path):
        print("Given Destination path is not of Directory/Folder")
        print("Please Provide correct path")
        return

    match="0"
    last=""
    objectPath=os.path.join(universal_dir_path,'.maruti','objects')
    cfiles=os.listdir(objectPath)

    for file in cfiles: 
         creation_time = os.path.getctime(f"{objectPath}/{file}")
         creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
         if(creation_time_readable>match):
            match=creation_time_readable
            last=file

    last_commit_path=f"{objectPath}/{last}"
    state={}

    with open(f"{last_commit_path}", 'r') as file:
        state = json.load(file)
    
    all={}
    all=state["all"]

    for file in all:
        decodedContent=base64.b64decode(all[file])
        file_path = os.path.join(dstn_path, file)

        with open(file_path, 'wb') as f:
            f.write(decodedContent)
    print("Done Successfully")

def checkout(hash_val):
    hashvalue=f"{hash_val}.json"
    
    if not os.path.exists(os.path.join(universal_dir_path,'.maruti','objects',hashvalue)):
        print("Given commit does not exist.")
        print("Please Provide correct hash value of commit which exists.")
        return 

    objectPath = os.path.join(universal_dir_path,'.maruti','objects')

    creation_time = os.path.getctime(f"{objectPath}/{hashvalue}")
    hashtime = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    cfiles=os.listdir(objectPath)

    for file in cfiles:
        creation_time = os.path.getctime(f"{objectPath}/{file}")
        creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        if(creation_time_readable>hashtime):
            os.remove(f"{objectPath}/{file}")
   
    state={}

    with open(f"{objectPath}/{hashvalue}", 'r') as file:
        state = json.load(file)
    
    all={}
    all=state["all"]

    all_file=os.listdir(universal_dir_path)

    for file in all_file:
          if(file=="main.py"):continue
          destination_path=os.path.join(universal_dir_path,file)
          if(os.path.isfile(os.path.join(universal_dir_path,file))):
              if file in all.keys():
                  decodedContent=base64.b64decode(all[file])

                  with open(destination_path, 'wb') as file:
                        file.write(decodedContent)
              else :
                os.remove(destination_path)
  
    print("Done Successfully")

def main():
    
    global universal_dir_path

    print("")
    print("Maruti - Version Control System")
    print("System Programming Project")
    print("- By Mr.Swet Lakhani")
    print("- DAIICT Student")
    
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
                print("The path you have given doesn't exists, kindly give path which exists...")
                print()
                universal_dir_path = None
                continue
            
            break
        elif ip == "2":
            exit()
        else :   
            print("")
            print("Enter valid input...")
            
    while True:
        
        user_input = input("Enter a command (type 'help' for usage): ").split()
        command = user_input[0]

        check = os.path.join(universal_dir_path,".maruti")

        if command == 'help':
            help()

        elif command == 'init':
            init(universal_dir_path)

        elif command == 'add':
            if not os.path.exists(check):
                print(".maruti Repository does not exists.")
                continue
            
            if len(user_input) > 1:
                file_name = user_input[1]
                add_command(file_name)
            else:
                print("Error: Specify a file to add.")

        elif command == 'status':
            if not os.path.exists(check):
                print(".maruti Repository does not exists.")
                continue
            
            status_command()

        elif command == 'commit':
            if not os.path.exists(check):
                print(".maruti Repository does not exists.")
                continue

            if len(user_input) > 2:
                if(user_input[1]=='-m'):
                    user_msg = " ".join(user_input[2:])
                    if not os.path.exists(check):
                        print(".maruti Repository does not exists.")
                        continue
                
                    commit(user_msg)
                else :
                    print("Error: Enter valid format to do commit")
            else :
                print("Error: Specify a message to add.")
                
        elif command == 'rmadd':
            if not os.path.exists(check):
                print(".maruti Repository does not exists.")
                continue
            
            rmadd_command()
               
        elif command == 'user':
            if not os.path.exists(check):
                print(".maruti Repository does not exists.")
                continue
    
            if len(user_input)>=2 and user_input[1]=="show":
                get_username()
            elif len(user_input)>=3 and user_input[1]=="set" : 
                new_user_name = ' '.join(user_input[2:])
                change_username(new_user_name)
            else:
                print("Enter valid syntax to show/change username")
        elif command == 'rmcommit': 
            if not os.path.exists(check):
                print(".maruti Repository does not exists.")
                continue
            rmcommit()
        elif command == 'log': 
            if not os.path.exists(check):
                print(".maruti Repository does not exists.")
                continue
            log()
        elif command == 'push': 
            if not os.path.exists(check):
                print(".maruti Repository does not exists.")
                continue
            if len(user_input)>=2:
                push(user_input[1])
            else:
                print("Enter valid syntax to push to a folder.")
        elif command == 'checkout': 
            if not os.path.exists(check):
                print(".maruti Repository does not exists.")
                continue
            if len(user_input)>=2:
                checkout(user_input[1])
            else :
                print("Enter valid syntax to perform checkout.")
        elif command == 'clear' or command == 'cls':
                clear()    
        elif command == 'exit':
            break
        else:
            print(f"Error: Unknown command '{command}'. Type 'help' for usage and to know correct Syntax")

if __name__ == "__main__":
    
    main()
    

