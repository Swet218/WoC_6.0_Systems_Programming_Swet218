import os
import json
import hashlib
import datetime

def clear_command():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_help():
    print("Usage:")
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
    print("Created by - Swet Lakhani")

def init_vcs(repo_path):
    username = input("Enter your username: ")

    vcs_dir = os.path.join(repo_path, '.maruti')
    
    branches_dir = os.path.join(vcs_dir, 'branches')
    main_branch_dir = os.path.join(branches_dir, 'main')
    objects_dir = os.path.join(vcs_dir, 'objects')
    added_json_path = os.path.join(main_branch_dir, 'added.json')
    index_json_path = os.path.join(main_branch_dir, 'index.json')
    users_txt_path = os.path.join(main_branch_dir, 'users.txt')
    
    if os.path.exists(vcs_dir):
        print("VCS Repository already exists.")
        return
    
    os.makedirs(main_branch_dir, exist_ok=True)
    os.makedirs(objects_dir, exist_ok=True)

    with open(added_json_path, 'w') as added_file:
        json.dump({}, added_file)
    with open(index_json_path, 'w') as index_file:
        json.dump({}, index_file)

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(users_txt_path, 'a') as users_file:
        users_file.write(f"{datetime.date.today()}, {timestamp}, {username}\n")

    print(f"Initialized repository at {repo_path}")

def calculate_file_hash_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            md5.update(chunk)
    return md5.hexdigest()

def add_command(filename):

    file_hash = calculate_file_hash_md5(filename)

    vcs_base_dir = os.path.join(os.getcwd(), '.maruti', 'branches', 'main')

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

def status_command():

    current_dir = os.getcwd()

    index_path = os.path.join(current_dir,'.maruti', 'branches', 'main', 'index.json')
    with open(index_path, 'r') as index_file:
        index_data = json.load(index_file)

    current_files = []
    for f in os.listdir('.'):
        if os.path.isfile(f):
            current_files.append(f)

    untracked_files = [file for file in current_files if file not in index_data or calculate_file_hash_md5(file) != index_data.get(file)]

    if untracked_files:
        print("Untracked files:")
        for file in untracked_files:
            print(f"- {file}")
    else:
        print("All files are tracked.")

def main():
    
    while True:
        user_input = input("Enter a command (type 'help' for usage): ").split()
        command = user_input[0]

        if command == 'help':
            print_help()
        elif command == 'init':
            repo_path = os.path.dirname(os.path.abspath(__file__))
            init_vcs(repo_path)
        elif command == 'add':
            # file_nam = input("Enter a file you want add :")
            # add_command(file_nam)
            if len(user_input) > 1:
                file_name = user_input[1]
                add_command(file_name)
            else:
                print("Error: Specify a file to add.")
        elif command == 'status':
            status_command()
        elif command == 'clear':
            clear_command()
        elif command == 'exit':
            break
        else:
            print(f"Error: Unknown command '{command}'. Type 'help' for usage.")

if __name__ == "__main__":
    main()
