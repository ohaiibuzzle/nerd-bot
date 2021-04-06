import json

def accountCheck(name):
    with open('accounts.json') as mainFile:
        file = json.load(mainFile)
        if str(name) in file:
            print("Your account already exists")
        else:
            accountCreate(name, 0, 0)

def accountCreate(name, score, points):   
    with open('accounts.json') as fileName:
        file = json.load(fileName)
        new_account = { name : {'score' : int(score), 'points' : int(points)}}
        file.update(new_account)
        with open('accounts.json', 'w') as fileEdit:
            json.dump(file, fileEdit, indent=4)
            print("Your account is now created! Enjoy")

def deleteAccount(name):
    with open('accounts.json') as f:
        json_file = json.load(f)
        json_file.pop(name)
        with open('accounts.json', 'w') as file:
            json.dump(json_file, file, indent=4)

create_account = input("Hey do you want to create an account [y/n]")
if create_account == "y":
    new_name = input("Please eter your name")
    accountCheck(new_name)
else:
    delete_account = input("So do you want to delete your account [y/n] ")
    if delete_account == "y":
        new_name = input("Please enter your name")
        deleteAccount(new_name)
        print("Aww.. We are sad to see you going.. But anyways will see you next time.")
        



