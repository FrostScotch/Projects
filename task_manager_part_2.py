# ========================Compulsory Task Part 2===============================
# =========================importing libraries=================================
from datetime import datetime

# =========================Login Section=======================================
credentials = {}
# Fetching existing credentials stored in text file.
with open('user.txt', 'r') as f:
    for line in f:
        # Splitting line into key and value.
        saved_username, saved_password = line.strip().split(", ")
        # Add the key-value pair to the dictionary.
        credentials[saved_username] = saved_password

# Prompt to user to input their login credentials.
# User provided login credntials are compared to those of registered users.
# Login is successful only if username and password match exactly to those
# on file.
print("========Task Management System Login=======")
login_username = input("Enter your username:\n")
while login_username not in credentials:
    login_username = input("User not found! Please enter a valid username:\n")
login_password = input("Enter your password:\n")
while credentials[login_username] != login_password:
    login_password = input("Invalid password for user! Please enter a valid"
                           " password:\n")
print("==============login Successful=============")

# =========================Main Program Section===============================
while True:
    # Present the menu of options to the user.
    print("===============Menu Options================")
    menu = input('''Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
vs - view statistics
e - exit
: ''').lower()

    # Option to register a new user.
    if menu == 'r':
        print("==========Registering New User===========")
        if login_username == "admin":
            new_user = input("Enter Username for new user:\n")
            new_password = input("Assign password for new user:\n")
            confirmed_password = input("Confirm assinged password:\n")

            # In case where the new assigned password does not match with
            # the confirmation of the password, user is continuously prompted
            # to input passwords until they match.
            while new_password != confirmed_password:
                print("Passwords do not match! Try entering password again.")
                new_password = input("Assign password for new user:\n")
                confirmed_password = input("Confirm assinged password:\n")
            with open('user.txt', 'a+') as f:
                f.write("\n" + new_user + ", " + new_password)
        else:
            print("User has no rights to register other users")

    # Option to add a task for user.
    # Task for user is stored in the 'tasks' text file.
    elif menu == 'a':
        print("==============Assigning Task==============")
        task_assignee = input("Enter username of assignee:\n")
        task_title = input("Enter the title of the task:\n")
        task_description = input("Enter the description of the task:\n")
        task_due_date = input("Enter the due date of the task in the format"
                              " 'DD MMM YYYY' e.g 10 Oct 2023:\n")
        # retrieving the current date in a specific format using python modules
        date_now = datetime.now()
        current_date = date_now.strftime("%d %b %Y")
        task_completion = "No"
        with open('tasks.txt', 'a+') as f:
            f.write("\n" + task_assignee + ", " + task_title + ", " +
                    task_description + ", " + task_due_date +
                    ", " + current_date + ", " + task_completion)

    # Option to view all tasks.
    # All tasks are retrieved from the text file 'tasks' line by line
    # and displayed.
    elif menu == 'va':
        print("=======Viewing All Assinged Tasks========")
        with open('tasks.txt', 'r+') as f:
            for line in f:
                task_attributes = line.strip('\n').split(", ")
                print("_________________________________________"
                      "__________________________________________"
                      "__________________________")
                print(f"Task:\t\t\t{task_attributes[1]}")
                print(f"Assigned to:\t\t{task_attributes[0]}")
                print(f"Date Assigned:\t\t{task_attributes[4]}")
                print(f"Due date:\t\t{task_attributes[3]}")
                print(f"Task Complete?\t\t{task_attributes[5]}")
                print("Task description:")
                print(f" {task_attributes[2]}")
        print("_________________________________________"
              "__________________________________________"
              "__________________________")

    # Option to view tasks specific to the logged in user.
    # Tasks specific to the logged in user are retrieved from the text
    # file 'tasks' line by line and displayed.
    # A flag is used to determine if user has tasks or not and display
    # the appropriate output.
    elif menu == 'vm':
        print("============Viewing User Task(s)===========")
        has_tasks = False
        with open('tasks.txt', 'r+') as f:
            for line in f:
                task_attributes = line.strip('\n').split(", ")
                if login_username == task_attributes[0]:
                    has_tasks = True
                    print("_________________________________________"
                          "__________________________________________"
                          "__________________________")
                    print(f"Task:\t\t\t{task_attributes[1]}")
                    print(f"Assigned to:\t\t{task_attributes[0]}")
                    print(f"Date Assigned:\t\t{task_attributes[4]}")
                    print(f"Due date:\t\t{task_attributes[3]}")
                    print(f"Task Complete?\t\t{task_attributes[5]}")
                    print("Task description:")
                    print(f" {task_attributes[2]}")
            if not has_tasks:
                print("==============Unassinged User=============")
                print("User has no tasks")
        print("_________________________________________"
              "__________________________________________"
              "__________________________")

    # Option to view user and tasks statics.
    # The number of users and tasks are obtained by counting the number of
    # lines in the respective text files.    
    elif menu == 'vs':
        print("===========Viewing User Statistics=========")
        number_of_users = 0
        number_of_tasks = 0
        if login_username == "admin":
            with open('user.txt', 'r') as f:
                for line in f:
                    if line.strip():
                        number_of_users += 1
            with open('tasks.txt', 'r') as f:
                for line in f:
                    if line.strip():
                        number_of_tasks += 1
            print("_________________________________________"
                  "__________________________________________"
                  "__________________________")
            print(f"Number of Registered Users:\t{number_of_users}")
            print(f"Number of Tasks:\t\t{number_of_tasks}")
        else:
            print("User has no rights to view statistics")
        print("_________________________________________"
              "__________________________________________"
              "__________________________")
    
    # Option to exit the program.
    elif menu == 'e':
        print("===================Exit==================")
        print('Goodbye!!!')
        break

    # Alternative syntax that executes in case an erroneous selection in
    # made in the main program.
    else:
        print("You have entered an invalid input. Please try again")