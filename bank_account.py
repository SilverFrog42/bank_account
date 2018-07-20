import hashlib
import os.path

accounts = {}
salt = []
words = ["hello", "pepper", "salty", "dog", "cat", "tiger", "qwerty", "free", "market", "economy", "you", "zebra", "deer", "hermit", "crab", "he", "we", "princeton", "technology", "innovation", "tea", "frog", "pug", "dumb", "lion", "entomology"]


def get_salt():
    file = open("salt_words.txt", "r")
    for line in file:
        salt.append(line)
    print(salt)

def salt_password(password):
    password = password.lower()
    last_letter = password[-1]
    if last_letter.isalnum():
        index = 0
    elif last_letter.isnumeric():
        index = int(last_letter)
    else:
        indexL = ord(last_letter)
        indexA = 97
        index = indexL - indexA
    salt = words[index]
    return salt


def read_file():
    if not os.path.isfile("accounts.txt"):
        return
    f = open("accounts.txt", "r")
    for line in f:
        words = line.split(" ")
        words.pop()
        accounts.update()
        username = words[0]
        password = words[1]
        PIN = words[2]
        balance = int(words[3])
        accounts.update({username: [password, PIN, balance]})
    f.close()

def write_file():
    f = open("accounts.txt", "a+")
    for username in accounts:
        f.write(username + " ")
        info = accounts[username]
        for item in info:
            f.write(str(item) + " ")
        f.write("\n")
    f.close()

def hasher(password):
    b = bytes(password, 'utf-8')
    m = hashlib.sha256(b)
    m = m.hexdigest()
    return m

def login():
    print("Logging in ")
    username = input("Please enter your username ")
    if not accounts.get(username):
        print("Please enter a valid username ")
        return

    password = input("Please enter your password ")
    password += salt_password(password)
    password = hasher(password)
    actual_password = accounts[username][0]
    actual_PIN = accounts[username][1]
    for i in range(0,6):
        password = input("Please enter your password ")
        password += salt_password(password)
        password = hasher(password)
        if i == 5:
            print("Locked out ")
            pmessage = input("Would you like to change your password? ")
            if pmessage == 'Yes':
                for i in range (0,6):
                    PIN = input("What is your PIN? ")
                    PIN = hasher(PIN)
                    if PIN == actual_PIN:
                        new_password = hasher(input("What would you like to change your password to? "))
                        accounts[username][0] = new_password
                        print("Your password has been changed ")
                        break
                    elif PIN != actual_PIN:
                        print("Sorry, that PIN is incorrect ")
                    if i == 5:
                        print("You have been locked out ")
            break
        if password == actual_password:
            print("Welcome, " + username + "!")
            message = input("Would you like to view your account? ")
            balance = accounts[username][2]
            if message == 'Yes':
                print("Your balance is ")
                print(balance)
            elif message == 'No':
                print("Alright, have a nice day ")
            message2 = input("Would you like to deposit or withdraw money? ")
            if message2 == 'D':
                newbalance = int(input("How much would you like to deposit? "))
                accounts[username][2] += newbalance
                print("Alright, your new balance is " + str(accounts[username][2]))
            elif message2 == 'W':
                newbalance = int(input("Alright, how much money would you like to withdraw? "))
                accounts[username][2] -= newbalance
                if newbalance > accounts[username][2]:
                    print("That is too much money to withdraw! ")
                if newbalance <= accounts[username][2]:
                    print("Alright, your new balance is " + str(accounts[username][2]))
            transfer_choice = input("Would you like to transfer money? ")
            if transfer_choice == 'Yes':
                user_transfer = input("Who would you like to transfer money to? ")
                transfer = int(input("How much money would you like to transfer?"))
                if transfer > accounts[username][2]:
                    print("That is too much money too transfer! ")
                if transfer <= accounts[username][2]:
                    accounts[username][2] -= transfer
                    accounts[user_transfer][2] += transfer

            break
        else:
            print("Wrong password- try again.")

get_salt()
salt_password("tea")
read_file()

message = input("Enter 'C' to create a new bank account, or press 'L' to login ")

while message != 'Q':

    if message == 'C':
        username = input("Create a username. ")
        while accounts.get(username):
            username = input("Username taken- please enter another one ")
        password = input("Create a password. ")
        password = password + salt_password(password)
        PIN = input("Please enter a PIN to secure your info. ")
        password = hasher(password)
        PIN = hasher(PIN)
        accounts.update({username : [password, PIN, 0]})

    if message == 'L':
        login()


    message = input("Enter 'C' to create a new bank account, or press 'L' to login ")

write_file()