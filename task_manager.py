class Task:
    def __init__(self, id, description, completed=False):
        self.id = id
        self.description = description
        self.completed = completed

    def __str__(self):
        status = "Done" if self.completed else "Pending"
        return f"[{self.id}] {self.description} - {status}"

class TaskManager:
    def __init__(self):
        self._tasks = []
        self._next_id = 1

    def add_task(self, description):
        task = Task(self._next_id, description)
        self._tasks.append(task)
        self._next_id += 1
        print(f"Task added: {task}")

    def list_tasks(self):
        if not self._tasks:
            print("No tasks available.")
            return
        for task in self._tasks:
            print(task)

    def complete_task(self, task_id):
        for task in self._tasks:
            if task.id == task_id:
                task.completed = True
                print(f"Task completed: {task}")
                return
        print(f"No task found with ID: {task_id}")

    def delete_task(self, task_id):
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                print(f"Task deleted: {task}")
                return
        print(f"No task found with ID: {task_id}")
    
    def delete_all_tasks(self):
        self._tasks.clear()
        print("All tasks have been deleted.")