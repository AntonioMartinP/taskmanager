from task_manager import TaskManager


def print_menu():
    print("\n---Welcome to the Task Manager!---")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Delete All Tasks")
    print("6. Exit")

def main():
    manager = TaskManager()

    while True:
        print_menu()
        choice_str = input("Enter your choice (1-6): ")
        try:
            choice = int(choice_str)
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 6.")
            continue

        match choice:
            case 1:
                description = input("Enter task description: ")
                manager.add_task(description)
            case 2:
                manager.list_tasks()
            case 3:
                task_id = int(input("Enter task ID to complete: "))
                manager.complete_task(task_id)
                
            case 4:
                task_id = int(input("Enter task ID to delete: "))
                manager.delete_task(task_id)


            case 5:
                manager.delete_all_tasks()
            case 6:
                print("Exiting Task Manager. Goodbye!")
                break
            case _:
                print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()