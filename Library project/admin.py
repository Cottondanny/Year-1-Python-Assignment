import json
from datetime import datetime
import os
import re
import pyfiglet

user_data = {'Member': [], 'Librarian': [], 'Admin': []}
user_type = None
user_database = 'accounts.txt'
def main_panel():
    picked_num = options()
    if picked_num == 1:
        member_manage()
    if picked_num == 2:
        librarian_manage()

def options(): #Main panel options
    generate_title('Welcome to Admin Panel')
    option_list = ['Member Account Management', 'Librarian Account Management']
    generate_options(option_list)

    #To make sure the input is only 1 and 2
    while True:
        picked_num = input(f'\033[93m[*]\033[0m Enter the number to manage the users: ')
        try:
            input_value = int(picked_num)

            if not 0 < input_value < 3:
                raise ValueError
            print()
            return input_value

        #To handle invalid inputs rather than integers
        except ValueError:
            print(f'\033[91m[ERROR] Invalid input! Please enter again.\033[0m')
            continue

def cmd_option(user_type): #Create the options for the admin's command
    options = f'''
    Available commands:
    - add: Add a new {user_type}
    - view: View {user_type} details
    - search: Search {user_type} information
    - edit: Edit {user_type} information
    - delete: delete a {user_type}
    - options: Show the available commnads
    - exit: Back to Main Menu
    '''
    print(options)

def save_data(): #To store the data into the database
    with open(user_database, 'w') as f:
        json.dump(user_data, f, indent=2)

def load_data(): #To load the data from the database
    global user_data
    try:
        if os.path.exists(user_database):
            with open(user_database, 'r') as f:
                user_data = json.load(f)
                return user_data
        else:
            user_data = {'Member': [], 'Librarian': [], 'Admin': []}
    except json.JSONDecodeError:
        user_data = {'Member': [], 'Librarian': [], 'Admin': []}

def generate_title(title): #Generate the title automatically
    title_txt = pyfiglet.figlet_format(title, font='shadow', width=300)
    print(f'\033[91m\033[1m{title_txt}\033[0m')

def generate_options(option_list): #Generate the option automatically
    number = 1
    for i in option_list:
        print(f'{number}. {i.title()}')
        number += 1
    print()

def generate_id():
    load_data()
    global user_type
    member_type = user_type.title()

    #To return default id value if there is no user in the database
    if not user_data[member_type]:
        return 101

    #To return the maximun value + 1 if the database has data.
    max_id = max(int(user['id'])for user in user_data[member_type])
    return max_id + 1

def member_manage(): #Member Management Panel
    generate_title('Member Account Management')
    print("\033[93m[*]\033[0m Use [options] to view the available commands.\n")

    while True:
        global user_type
        user_type = 'member'
        command = input(f'\033[91mAdmin\033[0m~# ').strip()
        if command == 'add':
            add_data()
        elif command == 'view':
            view_data()
        elif command == 'search':
            search_data()
        elif command == 'edit':
            edit_data()
        elif command == 'delete':
            delete_data()
        elif command == 'options':
            cmd_option(user_type)
        elif command == 'exit':
            print()
            main_panel()
        else:
            print(f"\033[91m[ERROR] Unknown command. Type 'options' for a list of available commands.\033[0m")

def librarian_manage(): #Librarian Management Panel
    generate_title('Librarian Account Management')
    print("\033[93m[*]\033[0m Use [options] to view the available commands.\n")

    while True:
        global user_type
        user_type = 'librarian'
        command = input(f'\033[91mAdmin\033[0m~# ').strip()
        if command == 'add':
            add_data()
        elif command == 'view':
            view_data()
        elif command == 'search':
            search_data()
        elif command == 'edit':
            edit_data()
        elif command == 'delete':
            delete_data()
        elif command == 'options':
            cmd_option(user_type)
        elif command == 'exit':
            print()
            main_panel()
        else:
            print(f"\033[91m[ERROR] Unknown command. Type 'options' for a list of available commands.\033[0m")

def role_validation(): #To validate the user role
    global user_type
    roles = ['member', 'librarian']
    while True:
        role = input('Enter the role: ').lower().strip()

        if user_type.lower() == 'member' and role == roles[0]: #Check the role is member
                return role
        elif user_type.lower() == 'librarian' and role == roles[1]:  # Check the role is member
                return role
        else:
            print(f'\033[91m[ERROR] Invalid role! Only "{user_type.lower()}" role is accepted.\033[0m')
            continue

def validate_data(pattern_key): #To validate the user information
    #Patterns to validate the input from the users
    global user_type
    member_type = user_type.title()
    patterns = {
        'full_name': re.compile(r'^[a-zA-Z0-9][\w\s.-_]{0,18}$'),
        'email': re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$'),
        'username': re.compile(r'^[a-zA-Z0-9][\w.-]{1,13}$'),
        'password': re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]{1,5})[A-Za-z\d@$!%*?&]{8,}$')
    }
    pattern = patterns.get(pattern_key)

    if not pattern: #If there is no valid pattern in 'patterns' dictionary
        raise ValueError('Invalid Pattern Key!')

    while True:
        input_value = input(f'Enter the {pattern_key}: ').strip()
        match = pattern.fullmatch(input_value) #Match the input with the specific pattern

        if match:
            if pattern_key == 'email':
                if any(user['email'] == input_value for user in user_data[member_type]):
                    print(f'\033[91m[ERROR] This email is already registered. Please use a different email.\033[0m')
                    continue
            if pattern_key == 'full_name':
                if any(user['full_name'] == input_value for user in user_data[member_type]):
                    print(f'\033[91m[ERROR] This name is already used. Please choose a different first name.\033[0m')
                    continue
            if pattern_key == 'username':
                if any(user['username'] == input_value for user in user_data[member_type]):
                    print(f'\033[91m[ERROR] This username is already used. Please choose a different username.\033[0m')
                    continue
            return input_value

        else: #Raise the errors when the pattern is not matched with the input
            error_messages = {
                'full_name': 'Only alphabets, digits, and hyphens are allowed! Maximum length is 20 characters.',
                'email': 'Invalid email address format! Example: example@domain.com',
                'username': 'Invalid Username! Maximum length is 15 characters. Example: user_name123',
                'password': 'The password must be at least 8 characters long and include:\n- At least one uppercase letter\n- At least one lowercase letter\n- At least one number\n- At least one special character (@, $, !, %, *, ?, &)'
            }
            print(f'\033[91m[ERROR] {error_messages.get(pattern_key, "Invalid input.")}\033[0m')

def show_data(data_list, counter): #Function to dispaly the searched data
    print()
    print(f'\033[42m {f'\033[30m\033[1m {'Id':<10} {'Full_name':<20} {'Email':<25} '
                      f'{'Username':<20} {'Password':<22} {'Role':<14} {'Registration_date':<20}\033[0m'} \033[0m')
    for data in data_list:
        print(
            f'  {data.get("id"):<10} {data.get("full_name"):<20} {data.get("email"):<25} '
            f'{data.get("username"):<20} {data.get("password"):<22} {data.get("role"):<14} {data.get("registration_date"):<20}')
    print()
    if counter == 0:
        print(f'\n\033[93m[*] No data found!\033[0m')
    if counter > 0:
        print(f'\033[93m[*]\033[0m {counter} user{"" if counter == 1 or 0 else "s"} found!')

def add_data(): #To add user data into the database
    try:
        load_data()
        global user_type
        member_type = user_type.title() #Store the user for later usage

        data = {
            'id': generate_id(),
            'full_name': validate_data('full_name'),
            'email': validate_data('email'),
            'username': validate_data('username'),
            'password': validate_data('password'),
            'role': role_validation(),
            'registration_date': datetime.now().strftime('%d-%B-%Y')
        }

        #Add the member into the 'user_data' and store that in database using 'save_data' function.
        user_data[member_type].append(data)
        save_data()
        print(f'\033[92m[*] The {member_type} has been created successfully.\033[0m\n')
    except Exception as e:
        # Handle unexpected errors
        print(f'\033[91m[ERROR] An error occurred while adding the data: {e}\033[0m')

def view_data(): #To view details information of the users
    load_data()
    global user_type
    member_type = user_type.title()
    show_data(user_data[member_type], len(user_data[member_type]))

def search_data(): #To search the users using a specific keyword
    load_data()
    global user_type
    member_type = user_type.title()

    while True:
        option_list = ['id', 'full_name', 'email', 'username', 'exit']
        search_key = input(f'\033[93m\n[*]\033[0m Options: (id, full_name, email, username, \'exit\' to quit)\n'
                            f'Which field would you like to search?: ').lower()

        if search_key == 'exit':
            print(f'\033[93m[*] Exiting the searching process.\033[0m\n')
            break

        try:
            if not search_key in option_list: #To check the input is in option_list(line263)
                raise ValueError

            counter = 0
            search_value = input('Enter the keyword to search: ')
            data_list = []

            for data in user_data[member_type]: #To search the user data using the re module
                match_data = re.search(search_value, str(data[search_key]), flags=re.IGNORECASE)

                if match_data:
                    data_list.append(data)
                    counter += 1

            show_data(data_list, counter)
        except ValueError:
            print(f'\033[91m[ERROR] Invalid option! Please enter the valid option.\033[0m')

def edit_data(): #To edit the user data using 'id'
    view_data()
    global user_type
    member_type = user_type.title()

    while True:
        id = input(f'\033[93m[*]\033[0m Enter the {user_type}\'s ID you want to edit (or type \'exit\' to quit): ').lower()

        if id == 'exit':
            print(f'\033[93m[*]\033[0m Exiting the editing process.\n')
            break
        try:
            max_id = max(int(data['id']) for data in user_data[member_type]) + 1
            valid_id = int(id)  # Check whether the id is integer and within the valid range
            if not 100 < valid_id < max_id:
                raise ValueError("ID out of acceptable range.")
            for data in user_data[member_type]:  # loop the data inside database to compare with the id
                if valid_id == data['id']:
                    while True:  # Allow to choose the options to edit the user information
                        choice_to_edit = input(
                            f'\n\033[93m[*]\033[0m Options: (full_name, email, username, password)\n'
                            f'\033[93m[*]\033[0m Which field would you like to update?: ').lower()
                        option_list = ['full_name', 'email', 'username', 'password',]
                        if choice_to_edit in option_list:  # Check the input option is valid or not
                            edited_data = validate_data(choice_to_edit)
                            data[choice_to_edit] = edited_data
                            save_data()
                            print(f'\033[92m[*] The {member_type} has been edited successfully.\033[0m')

                            while True:
                                still_edit = input(f'\033[93m[*]\033[0m Do you want to continue editing this {member_type}? '
                                                   f'(Press \'n\' -> No, \'y\' -> Yes): ').lower()
                                if still_edit in ['y', 'n']:
                                    break
                                print(f'\033[91m[ERROR] Invalid option! Please enter again.\033[0m')
                            if still_edit == 'y':
                                continue
                            elif still_edit == 'n':
                                break

                        else:
                            print(f'\033[91m[ERROR] Invalid option! Please enter again.\033[0m')
                    break
            else:
                print(f'\033[91m[ERROR] The ID {valid_id} does not exist in the database. Please enter again.\033[0m')
        except ValueError:
            print(f'\033[91m[ERROR] Invalid ID! Please enter a valid ID, or ensure the ID exists in the database.\033[0m')

def delete_data(): #Delete the user data from the database using 'id'
    load_data()
    global user_type
    member_type = user_type.title()

    while True:
        id = input(f'\033[93m[*]\033[0m Enter the {member_type}\'s ID you want to delete (or type \'exit\' to quit): ')

        if id == 'exit':
            print(f'\033[93m[*] Exiting the deleting process.\033[0m\n')
            break

        try: #Try to validate the id before remove from the database
            max_id = max(int(id['id']) for id in user_data[member_type]) + 1
            valid_id = int(id)
            if not 100 < valid_id < max_id: #To make sure the id is within the valid range
                raise ValueError
            for data in user_data[member_type]: #Find the id and remove from the database
                if valid_id == data['id']:
                    user_data[member_type].remove(data)

                    counter_id = 101 #Rearrange the id number after deleting the user
                    for user in user_data[member_type]:
                        user['id'] = counter_id
                        counter_id += 1
                    save_data()
                    print(f'\033[92m[*] The {member_type} has been deleted successfully.\033[0m')

        except ValueError:
            print(f'\033[91m[ERROR] Invalid ID! Please enter a valid ID, or ensure the ID exists in the database.\033[0m')

if __name__ == '__main__':
    main_panel()
