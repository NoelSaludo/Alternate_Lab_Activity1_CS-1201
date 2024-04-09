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
        if localUsers["admin"] != password:
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
        print("4. Admin Login")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            os.system("cls")
            showRentalTimes()
            input("Press any key to continue...")
        elif choice == "2":
            os.system("cls")
            login()
        elif choice == "3":
            os.system("cls")
            register()
        elif choice == "4":
            os.system("cls")
            adminLogin()
        elif choice == "5":
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
        choice = input("Enter your choice: ")
        if not choice:
            return
        if not choice.isdigit():
            print("Invalid choice. Please try again.")
            continue
        choice = int(choice)
        if choice == 0:
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
        if not amount:
            return
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
        break
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
def AddNewRentalTime():
    while True:
        print("Add new rental time")
        print("Enter 0 to go back")
        time = input("Enter rental time in hours: ")
        if time == "0":
            break
        if not time.isdigit():
            print("Invalid time. Please try again.")
            continue
        if not time:
            return
        time = int(time)
        if time <= 0:
            print("Invalid time. Please try again.")
            continue
        price = input("Enter price: ")
        if not price.isdigit():
            print("Invalid price. Please try again.")
            continue
        if not price:
            return
        price = int(price)
        if price <= 0:
            print("Invalid price. Please try again.")
            continue
        if f"{time} Hours" in rentalTimes:
            print("Rental time already exists. Please try again.")
            continue
        rentalTimes[f"{time} Hours"] = {"Time": time, "Price": price}
        print("Rental time added successfully.")
        input("Press any key to continue...")
        break
def ModifyRentalTime():
    while True:
        print("Modify rental time")
        print("Enter 0 to go back")
        showRentalTimes()
        listofTimes = list(rentalTimes.keys())
        choice = input("Enter your choice: ")
        if not choice.isdigit():
            print("Invalid choice. Please try again.")
            continue
        choice = int(choice)
        if choice == 0:
            break
        if choice > len(listofTimes):
            print("Invalid choice. Please try again.")
            continue
        time = listofTimes[choice-1]
        newTime = input("Enter new rental time in hours: ")
        if not newTime.isdigit():
            print("Invalid time. Please try again.")
            continue
        if not newTime:
            return
        newTime = int(newTime)
        if newTime <= 0:
            print("Invalid time. Please try again.")
            continue
        newPrice = input("Enter new price: ")
        if not newPrice.isdigit():
            print("Invalid price. Please try again.")
            continue
        if not newPrice:
            return
        newPrice = int(newPrice)
        if newPrice <= 0:
            print("Invalid price. Please try again.")
            continue
        rentalTimes[f"{newTime} hours"] = {"Time": newTime, "Price": newPrice}
        del rentalTimes[time]
        print("Rental time modified successfully.")
        input("Press any key to continue...")
        break
def RemoveRentalTime():
    while True:
        print("Remove rental time")
        print("Enter 0 to go back")
        showRentalTimes()
        listofTimes = list(rentalTimes.keys())
        choice = input("Enter your choice: ")
        if not choice.isdigit():
            print("Invalid choice. Please try again.")
            continue
        choice = int(choice)
        if choice == 0:
            break
        if choice > len(listofTimes):
            print("Invalid choice. Please try again.")
            continue
        time = listofTimes[choice-1]
        del rentalTimes[time]
        print("Rental time removed successfully.")
        input("Press any key to continue...")
        break
def adminMenu():
    global isAdminLogin
    while isAdminLogin:
        os.system("cls")
        print("Welcome Admin")
        print("1. Add new rental time")
        print("2. Modify rental time")
        print("3. Remove rental time")
        print("4. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            os.system("cls")
            AddNewRentalTime()
        elif choice == "2":
            os.system("cls")
            ModifyRentalTime()
        elif choice == "3":
            os.system("cls")
            RemoveRentalTime()
        elif choice == "4":
            isAdminLogin = False
            break
        else:
            os.system("cls")
            print("Invalid choice. Please try again.")
def app():
    while True:
        os.system("cls")
        mainMenu()
        userMenu()
        adminMenu()
    pass

app()