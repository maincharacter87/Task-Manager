# ========================================= CAPSTONE PROJECT 3 =======================================

# =========== Importing Libraries ===========
from datetime import datetime

# =========== Defining Functions ===========

# Register user function
def reg_user():
    register = False
    while register == False:
        new_user = input("Enter the username: ")
        if new_user in login_credentials:
            print("This username already exists. Try a different username.")
        else:
            new_password = input("Enter password: ")
            confirm = input("Confirm password: ")
            if new_password == confirm:
                with open("user.txt", "a") as user_file:
                    user_file.write(f"\n{new_user}, {new_password}")
                    login_credentials[new_user] = confirm
                print("You have registered a new user with username: {}".format(new_user))
                register = True
            else:
                print("The passwords you have entered do not match.")

# Add task function
def add_task():
    user_assigned = input("Enter the username of the person you are assigning the task to: ")
    if user_assigned in login_credentials:
        task_title = input("Enter the task title: ")
        task_description = input("Enter a description of the task: ")
        due_date_string = input("Enter the task due date (dd/mm/yyyy): ")
        due_date_object = datetime.strptime(due_date_string, "%d/%m/%Y")
        task_due_date = due_date_object.strftime("%d %b %Y")
        today = datetime.now()
        task_assigned_date = today.strftime("%d %b %Y")
        completion_status = "No"
        user_assigned_list.append(user_assigned)
        task_title_list.append(task_title)
        task_description_list.append(task_description)
        task_assigned_date_list.append(task_assigned_date)
        task_due_date_list.append(task_due_date)
        completion_status_list.append(completion_status)
        with open("tasks.txt", "a") as file:
            file.write(f"\n{user_assigned}, {task_title}, {task_description}, {task_assigned_date}, {task_due_date}, {completion_status}")
            print("You have successfully added a task with title {} to the user with username {}".format(task_title, user_assigned))
    else:
        print("The user you have specified is not registered. You will now be returned to the main menu.")

# View all tasks function
def view_all():
    for i in range(len(user_assigned_list)):
        print(f'''
---------------------------------------------------------                      
        Task              :  {(task_title_list[i])}
        Assigned to       :  {(user_assigned_list[i])}
        Date assigned     :  {(task_assigned_date_list[i])}
        Due date          :  {(task_due_date_list[i])}
        Task complete     :  {(completion_status_list[i])}
        Task description  :  {task_description_list[i]}\n

-------------------------_-------------------------------
''')
        
# Finding index of a task function
''' This function will take in the user choice of 'my task number' to edit
and return the index of this item in the list of all tasks (master list)'''
def find_master_index(choice):
    my_task_num = 0
    master_index_dict = {}
    for i in range(len(user_assigned_list)):
        if username == user_assigned_list[i]:
            my_task_num += 1
            master_index_dict[my_task_num] = i
    index = master_index_dict[choice]
    return index

# View My Task Function
def view_mine():
    my_task_num = 0
    for i in range(len(user_assigned_list)):
            if username == user_assigned_list[i]:
                my_task_num += 1
                print(f'''
---------------------------------------------------------  
                My Task Number:     {my_task_num}
                Task:               {(task_title_list[i])}
                Assigned to:        {(user_assigned_list[i])}
                Date assigned:      {(task_assigned_date_list[i])}
                Due date:           {(task_due_date_list[i])}
                Task complete?      {(completion_status_list[i])}
                Task description:   {task_description_list[i]}\n
---------------------------------------------------------  
''')

# This function will generate reports on the tasks and users  in the task manager and write them to two text files
def generate_reports():
    total_users = len(login_credentials)
    total_tasks = len(task_title_list)
    completed_tasks = len([task for task in completion_status_list if task == "Yes"])
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = len([datetime.strptime(date, '%d %b %Y') for date, task_completed in zip(task_due_date_list, completion_status_list) if task_completed == "No" and datetime.strptime(date, '%d %b %Y') < datetime.now()])
    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100
    overdue_percentage = (overdue_tasks / total_tasks) * 100
    # Write task_overview report to text file
    with open("task_overview.txt", "w") as f:
        f.write(f"Task Overview\n")
        f.write(f"Total number of tasks: {total_tasks}\n")
        f.write(f"Total number of completed tasks: {completed_tasks}\n")
        f.write(f"Total number of uncompleted tasks: {uncompleted_tasks}\n")
        f.write(f"Total number of tasks that are overdue: {overdue_tasks}\n")
        f.write(f"Percentage of tasks that are incomplete: {incomplete_percentage:.2f}%\n")
        f.write(f"Percentage of tasks that are overdue: {overdue_percentage:.2f}%\n\n")
    # Write user_overview report to text file
    with open("user_overview.txt", "w") as f:
        f.write(f"User Overview\n")
        f.write(f"Total number of users: {total_users}\n")
        f.write(f"Total number of tasks: {total_tasks}\n\n")
        for user in login_credentials:
            user_tasks = len([task for task in zip(task_title_list, user_assigned_list) if task[1] == user])
            user_task_percentage = (user_tasks / total_tasks) * 100
            if user_tasks == 0: # Include this if statement to prevent a division by zero error if the user has no tasks
                user_completed_percentage = 0
                user_overdue_percentage = 0
            else:
                user_completed_percentage = len([task for task, status in zip(task_title_list, completion_status_list) if status == "Yes" and task in task_title_list and user_assigned_list[task_title_list.index(task)] == user]) / user_tasks * 100
                user_uncompleted_percentage = 100 - user_completed_percentage
                user_overdue_percentage = len([task for task, status in zip(task_due_date_list, completion_status_list) if status == "No" and datetime.strptime(task, '%d %b %Y') < datetime.now() and user_assigned_list[task_due_date_list.index(task)] == user]) / user_tasks * 100
            f.write(f"{user}:\n")
            f.write(f"\tTotal number of tasks assigned: {user_tasks}\n")
            f.write(f"Percentage of total tasks assigned: {user_task_percentage:.2f}%\n")
            f.write(f"Percentage of assigned tasks completed: {user_completed_percentage:.2f}%\n")
            f.write(f"Percentage of assigned tasks uncompleted: {user_uncompleted_percentage:.2f}%\n")
            f.write(f"Percentage of assigned tasks overdue: {user_overdue_percentage:.2f}%\n\n")
    print("Reports successfully generated.")

# Program reads the user.txt file and writes contents to key : value pairs in a login_credentials dictionary
with open("user.txt" , "r") as file:
    contents = file.readlines()
    login_credentials = {}
    for line in contents:
        key, value = line.strip().split(", ")
        login_credentials[key] = value

# Program reads the tasks.txt file and writes contents to lists
user_assigned_list = []
task_title_list = []
task_description_list = []
task_assigned_date_list = []
task_due_date_list = []
completion_status_list = []
with open("tasks.txt", "r") as file:
    for lines in file:
        temp = lines.strip("\n")
        temp = temp.split(", ")
        user_assigned_list.append(temp[0])
        task_title_list.append(temp[1])
        task_description_list.append(temp[2])
        task_assigned_date_list.append(temp[3])
        task_due_date_list.append(temp[4])
        completion_status_list.append(temp[5])

# Login section
login = False
while login == False:
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in login_credentials and password == login_credentials[username]:
            login = True
            print("You are logged in as {}.".format(username))
            break
    else:
        print("You have not entered a valid username and/or password.")

# Display menu to user
# If the user is the administrator they have the added options to register new users and display statistics whereas regular users do not
while True:
    if username == "admin":
        menu = input('''Select one of the following options below:
                r - Registering a user
                a - Adding a task
                va - View all tasks
                vm - View my task
                gr - Generate reports
                ds - Display statistics
                e - Exit
                :''').lower()
    else: 
        menu = input('''Select one of the following Options below:
        a - Adding a task
        va - View all tasks
        vm - View my task
        e - Exit
        : ''').lower()

# Menu options:
    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
        while True:
            choice = int(input("Enter a task number to edit or -1 to return to main menu: "))
            if choice == -1:
                break
            else:
                index = find_master_index(choice)
                if completion_status_list[index] == "No":
                    action = input('''Select an action:
                                - Mark task as complete (enter 'complete') OR 
                                - Edit the user assigned or due date (enter 'edit'):''').lower()
                    if action == 'complete':
                        completion_status_list[index] = "Yes"
                        with open("tasks.txt", "w") as file:
                            for i in range(len(user_assigned_list)):
                                file.write(f"{user_assigned_list[i]}, {task_title_list[i]}, {task_description_list[i]}, {task_assigned_date_list[i]}, {task_due_date_list[i]}, {completion_status_list[i]}\n")
                        print(f"You have marked task '{task_title_list[index]}' as complete.")
                    elif action == 'edit':
                        type_of_edit = input('''Select an action:
                                        - Edit the user assigned (enter 'user') OR
                                        - Edit the due date enter (enter 'date'): ''')
                        if type_of_edit == "user":
                            user_edit = input("Enter the username of the user you would like this task reassigned to: ").lower()
                            if user_edit in login_credentials:
                                user_assigned_list[index] = user_edit
                                with open("tasks.txt", "w") as file:
                                    for i in range(len(user_assigned_list)):
                                        file.write(f"{user_assigned_list[i]}, {task_title_list[i]}, {task_description_list[i]}, {task_assigned_date_list[i]}, {task_due_date_list[i]}, {completion_status_list[i]}\n")
                                print(f"You have assigned the task to the user with username: {user_assigned_list[index]}")
                            else:
                                print("This user does not exist.")
                                print("You will now be returned to the main menu.")
                                break
                        elif type_of_edit == "date":
                            date_edit_string = input("Enter the task due date (dd/mm/yyyy): ")
                            date_edit_object = datetime.strptime(date_edit_string, "%d/%m/%Y")
                            date_edit = date_edit_object.strftime("%d %b %Y")
                            task_due_date_list[index] = date_edit
                            with open("tasks.txt", "w") as file:
                                for i in range(len(user_assigned_list)):
                                        file.write(f"{user_assigned_list[i]}, {task_title_list[i]}, {task_description_list[i]}, {task_assigned_date_list[i]}, {task_due_date_list[i]}, {completion_status_list[i]}\n")
                            print(f"You have changed the due date to {date_edit}")
                    else:
                        print("You have not specificed a valid action and will now be returned to the main menu.")
                        break
                elif completion_status_list[index] == "Yes":
                    print('''You can't edit this due date as it has already been completed.
                    You will now be returned to the main menu.''')
    # Viewing statistics (total number of tasks and total number of users read from task_overview and user_overview)
    elif menu == "ds":
        generate_reports()
        print("\n")
        # Output contents of task_overview file
        with open("task_overview.txt", "r") as file:
            for line in file:
                print(line)
        # Output contents of user_overview file
        with open("user_overview.txt", "r") as file:
            for line in file:
                print(line)
    elif menu == 'gr':
        generate_reports()
    elif menu == 'e':
        print("Goodbye!")
        break
