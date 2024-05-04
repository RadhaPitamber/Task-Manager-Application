import datetime

# Global variable to store logged-in user
logged_in_user = None

# Login Function
def login():
    global logged_in_user
    while True:
        username_input = input("Enter your username: ")
        password_input = input("Enter your password: ")

        # Read usernames and passwords from user.txt
        with open("user.txt", "r") as user_file:
            users_data = [line.strip().split(", ") for line in user_file]

        valid_credentials = False
        for user in users_data:
            if username_input == user[0] and password_input == user[1]:
                valid_credentials = True
                logged_in_user = username_input
                break

        if valid_credentials:
            return

        print("Invalid username or password. Please try again.")

# Check if the logged-in user is the admin
def is_admin(username):
    return username == 'admin'

# Main menu loop
while True:
    if not logged_in_user:
        login()

    # Present the menu to the user and make sure that the user input is converted to lower case.
    menu = input(f'''Select one of the following options:

    {'r - register a user\n' if is_admin(logged_in_user) else ''}
    a - add task
    va - view all tasks
    vm - view my tasks
    {'s - display statistics\n' if is_admin(logged_in_user) else ''}
    e - exit
    : ''').lower()

    if menu == 'r' and is_admin(logged_in_user):
        # Code to register a new user
        new_username = input("Enter a new username: ")
        new_password = input("Enter a new password: ")
        confirm_password = input("Confirm the password: ")

        if new_password == confirm_password:
            with open("user.txt", "a") as user_file:
                user_file.write(f"\n{new_username}, {new_password}")
            print("User registered successfully.")
        else:
            print("Passwords do not match. Please try again.")

    elif menu == 'a':
        # Code to add a new task
        assignee_username = input("Enter the username of the person the task is assigned to: ")

        # Validate if the user exists
        with open("user.txt", "r") as user_file:
            users_data = [line.strip().split(", ") for line in user_file]

        user_exists = any(user[0] == assignee_username for user in users_data)
        if not user_exists:
            print("Error: User does not exist.")
            continue

        task_title = input("Enter the title of the task: ")
        task_description = input("Enter the description of the task: ")
        due_date = input("Enter the due date of the task (YYYY-MM-DD): ")

        # Get the current date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        # Add the task data to tasks.txt
        with open("tasks.txt", "a") as tasks_file:
            tasks_file.write(f"\n{assignee_username}, {task_title}, {task_description}, {current_date}, {due_date}, No")

        print("Task added successfully.")

    elif menu == 'va':
        # Code to view all tasks
        with open("tasks.txt", "r") as tasks_file:
            tasks_data = [line.strip().split(", ") for line in tasks_file]

        for task in tasks_data:
            print(f"Assigned to: {task[0]}\nTitle: {task[1]}\nDescription: {task[2]}\nDate Assigned: {task[3]}\nDue Date: {task[4]}\nStatus: {task[5]}\n")

    elif menu == 'vm':
        # Code to view tasks assigned to the current user
        with open("tasks.txt", "r") as tasks_file:
            tasks_data = [line.strip().split(", ") for line in tasks_file]

        for task in tasks_data:
            if logged_in_user == task[0]:
                print(f"Title: {task[1]}\nDescription: {task[2]}\nDue Date: {task[4]}\nStatus: {task[5]}\n")

    elif menu == 's' and is_admin(logged_in_user):
        # Code to display statistics
        with open("user.txt", "r") as user_file:
            total_users = len(user_file.readlines())

        with open("tasks.txt", "r") as tasks_file:
            total_tasks = len(tasks_file.readlines())

        print(f"Total number of users: {total_users}\nTotal number of tasks: {total_tasks}")

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have entered an invalid input. Please try again")
