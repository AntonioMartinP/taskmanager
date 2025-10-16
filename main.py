from task_manager import TaskManager
from ai_service import create_simple_tasks



def print_menu():
    print("\n---Welcome to the Task Manager!---")
    print("1. Add Task")
    print("2. Añadir tarea complega con IA")
    print("3. List Tasks")
    print("4. Complete Task")
    print("5. Delete Task")
    print("6. Delete All Tasks")
    print("7. Exit")

def main():
    manager = TaskManager()

    while True:
        print_menu()
        choice_str = input("Enter your choice (1-7): ")
        try:
            choice = int(choice_str)
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 7.")
            continue

        match choice:
            case 1:
                description = input("Enter task description: ")
                manager.add_task(description)
            case 2:
                description=input("Descripcion de la tarea compleja: ")
                subtasks=create_simple_tasks(description)
                for subtask in subtasks:
                    if not subtask.startswith("Error:"):
                    
                        manager.add_task(subtask)
                    else:
                        print(subtask)
                        break

            case 3:
                try:
                    manager.list_tasks()
                except Exception as e:
                    print("Error al listar tareas:", e)
                input("Pulsa Enter para continuar...")
            case 4:
                task_id = int(input("Enter task ID to complete: "))
                manager.complete_task(task_id)
                
            case 5:
                task_id = int(input("Enter task ID to delete: "))
                manager.delete_task(task_id)


            case 6:
                manager.delete_all_tasks()
            case 7:
                print("Exiting Task Manager. Goodbye!")
                break
            case _:
                print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()