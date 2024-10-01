import json

#pre-loaded accounts
pre_accounts =  { "users": [
        {
  "Member": [
    {
      "id": 101,
      "full_name": "Jame Bob",
      "email": "jame@mail.com",
      "username": "Jame_bob",
      "password": "Jame1234@",
      "role": "member",
      "registration_date": "30-September-2024"
    },
    {
      "id": 102,
      "full_name": "Ray Nayon",
      "email": "Ray@yahoo.com",
      "username": "ray_Nax",
      "password": "Ray*1125",
      "role": "member",
      "registration_date": "30-September-2024"
    },
    {
      "id": 103,
      "full_name": "Howard",
      "email": "howard@gmail.com",
      "username": "Howard_223",
      "password": "Howard1!",
      "role": "member",
      "registration_date": "30-September-2024"
    }
  ],
  "Librarian": [
    {
      "id": 101,
      "full_name": "Ying Q",
      "email": "ying@mail.com",
      "username": "Yin_Q",
      "password": "Yin1928$",
      "role": "librarian",
      "registration_date": "30-September-2024"
    },
    {
      "id": 102,
      "full_name": "Groot",
      "email": "root@mail.com",
      "username": "g_Root",
      "password": "gRoot929&",
      "role": "librarian",
      "registration_date": "30-September-2024"
    }
  ],
  "Admin": [
    {
      "id": 101,
      "full_name": "Lb_admin",
      "email": "admin@mail.com",
      "username": "super_admin",
      "password": "$dmin@99834",
      "role": "admin",
      "registration_date": "30-September-2024"
    }
  ]
}
    ]
}
#for storing the pre-loaded accounts
with open('accounts.txt','w') as file:
    json.dump(pre_accounts,file, indent=4)

#for loading user data for login
def load_users():
    with open('accounts.txt','r') as file:
       return json.load(file)
    
#for login veriication
def login_users(data):
    while True:
        username = input('enter your email address: ')
        password = input('enter your password: ')

        for category in data["users"][0].values():
            for user in category:
                if user["email"] == username and user["password"] == password:
                    print(f"login successful! welcome {user['username']} role: {user['role']}")
                    return user
        print("invalid email or password, try again")

#for admin interface
def system_admin():
    while True:
        print("1. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("You have been logged out. Returning to login page...")
            return
             # Go back to the login page

# for librarian interface
def librarian():
    while True:
        print("1. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("You have been logged out. Returning to login page...")
            return
            
# for member interface
def library_member():
    while True:
        print("1. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("You have been logged out. Returning to login page...")
            return

def select_interface(user):
    interface = user["role"]

    if interface == "admin":
        system_admin()
    elif interface == "librarian":
        librarian()
    elif interface == "member":
        library_member()

def main():
    account_data = load_users()

    while True:
        user = login_users(account_data)
        if user:
            select_interface(user)


main()