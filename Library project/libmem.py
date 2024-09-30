import json
import pyfiglet

s='Welcome!'
text = pyfiglet.figlet_format(s, font='varsity')
print(text)

tologin={
    "login_info": [
        {"username": "Danny",
        "password": "danny123"
        },
        {"username": "Robin",
        "password": "robin123"
        },
        {"username": "pewdiepie",
        "password": "brofist"
        }
    ]
}



json_string =json.dumps(tologin, indent=2)
with open('userdata.json', 'w') as f:
    f.write(json_string)


def libmeminterface():
    print('WELCOME USER!')
    print('-------------')
    print('1. Search books')
    print('2. View loaned books')
    print('3. Update profile')
    print('4. Logout')
    action=int(input('Enter options: '))
    
    #now the actions
    while action >4:
        print('You must enter a number.')
        action=int(input('Enter options: '))
        
    if action==1:
        searchbooks()
    elif action==2:
        viewloaned()
    elif action==3:
        updateprofile()
    else:
        logout()

#need to create defs for the actions 




    

        


libmeminterface()


