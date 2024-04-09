import os, time, datetime, threading, msvcrt

rentalTimes = {"1 Hour": {"Time": 1, "Price": 15}, 
               "2 Hours": {"Time": 2, "Price": 30},
               "3 Hours": {"Time": 3, "Price": 40},
               "4 Hours": {"Time": 4, "Price": 55}
}
localUsers = {"admin": "adminpass"}
isUserLogin = False
isAdminLogin = False
stopTimer = False
CurrentUser = ""
def timer(h):
    total_seconds = h * 3600
    while total_seconds >= 0:
        timer = datetime.timedelta(seconds= total_seconds)
        if stopTimer:
            break
        os.system("cls")
        print(timer)
        print("Press Enter to stop timer")
        time.sleep(1)
        total_seconds -= 1
def stopTimerOnInput():
    global stopTimer
    while True:
        if msvcrt.kbhit():
            if msvcrt.getch() == b'\r':  # b'\r' is the Enter key in bytes
                stopTimer = True
                break
def showRentalTimes():
    print("Rental Times")
    for key in rentalTimes:
        print(key, ":", rentalTimes[key]["Price"])
def register():
    while True:
        print("Register")
        username = input("Enter username: ")
        if not username:
            return
        if username in localUsers:
            print("Username already exists. Please try again.")
            continue
        password = input("Enter password: ")
        if not password:
            print("Password cannot be empty. Please try again.")
            continue
        localUsers[username] = {"password": password, "balance": 15}
        break
def login():
    global isUserLogin, CurrentUser
    while True:
        print("Login")
        username = input("Enter username: ")
        if not username:
            return
        if username not in localUsers:
            print("Username does not exist. Please try again.")
            continue
        password = input("Enter password: ")
        if not password:
            print("Password cannot be empty. Please try again.")
            continue
        if localUsers[username]["password"] != password:
            print("Invalid password. Please try again.")
            continue
        CurrentUser = username
        isUserLogin = True
        break
def adminLogin():
    global isAdminLogin
    while True:
        print("Admin Login")
        username = input("Enter username: ")
        if not username:
            return
        if username != "admin":
            print("Username does not exist. Please try again.")
            continue
        password = input("Enter password: ")
        if not password:
            print("Password cannot be empty. Please try again.")
            continue
        if localUsers["admin"]["password"] != password:
            print("Invalid password. Please try again.")
            continue
        isAdminLogin = True
        break

def mainMenu():
    while not isUserLogin and not isAdminLogin:
        os.system("cls")
        print("Welcome to CompShopRentals")
        print("1. Show Rental times")
        print("2. Login")
        print("3. Register")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            os.system("cls")
            showRentalTimes()
        elif choice == "2":
            os.system("cls")
            login()
        elif choice == "3":
            os.system("cls")
            register()
        elif choice == "4":
            exit(0)
        else:
            os.system("cls")
            print("Invalid choice. Please try again.")
def RentComputer():
    global CurrentUser
    os.system("cls")
    while True:
        print("Rent a computer")
        print("Enter 0 to go back")
        showRentalTimes()
        listofTimes = list(rentalTimes.keys())
        choice = int(input("Enter your choice: "))
        if choice == "0":
            break
        if choice > len(listofTimes):
            print("Invalid choice. Please try again.")
            continue
        rentedTime = rentalTimes[listofTimes[choice-1]]["Time"]
        price = rentalTimes[listofTimes[choice-1]]["Price"]
        if localUsers[CurrentUser]["balance"] < price:
            print("Insufficient balance. Please top up your balance.")
            input("Press any key to continue...")
            continue
        localUsers[CurrentUser]["balance"] -= price
        timerThread = threading.Thread(target=timer, args=(rentedTime,))
        timerThread.start()
        stopTimerOnInput()
        break
def TopUpBalance():
    global CurrentUser
    os.system("cls")
    while True:
        print("Top up balance")
        print("Enter 0 to go back")
        print(f"Your current balance is {localUsers[CurrentUser]['balance']}")
        amount = input("Enter amount to top up: ")
        if not amount.isdigit():
            print("Invalid amount. Please try again.")
            continue
        if not amount:
            return
        amount = int(amount)
        if amount <= 0:
            print("Invalid amount. Please try again.")
            continue
        localUsers[CurrentUser]["balance"] += amount
        print("Balance topped up successfully.")
        input("Press any key to continue...")
    pass
def userMenu():
    global isUserLogin
    while isUserLogin:
        os.system("cls")
        print(f"Welcome {CurrentUser}")
        print("1. Rent a computer")
        print("2. Top up balance")
        print("3. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            RentComputer()
        elif choice == "2":
            TopUpBalance()
        elif choice == "3":
            isUserLogin = False
            break
        else:
            os.system("cls")
            print("Invalid choice. Please try again.")
def app():
    while True:
        os.system("cls")
        mainMenu()
        userMenu()
    pass

app()