import json
import os

class Task:
    def __init__(self, id, description, completed=False):
        self.id = id
        self.description = description
        self.completed = completed

    def __str__(self):
        status = "Done" if self.completed else "Pending"
        return f"[{self.id}] {self.description} - {status}"

    def to_dict(self):
        return {"id": self.id, "description": self.description, "completed": self.completed}

    @staticmethod
    def from_dict(d):
        return Task(d["id"], d["description"], d.get("completed", False))

class TaskManager:
    FILENAME = "tasks.json"

    def __init__(self):
        self._tasks = []
        self._next_id = 1
        self.load_tasks()

    def add_task(self, description):
        task = Task(self._next_id, description)
        self._tasks.append(task)
        self._next_id += 1
        self.save_tasks()
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
                self.save_tasks()
                print(f"Task completed: {task}")
                return
        print(f"No task found with ID: {task_id}")

    def delete_task(self, task_id):
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                removed = self._tasks.pop(i)
                self.save_tasks()
                print(f"Task deleted: {removed}")
                return
        print(f"No task found with ID: {task_id}")

    def delete_all_tasks(self):
        self._tasks.clear()
        self._next_id = 1
        self.save_tasks()
        print("All tasks have been deleted.")

    def load_tasks(self):
        if not os.path.exists(self.FILENAME):
            self._tasks = []
            self._next_id = 1
            return
        try:
            with open(self.FILENAME, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self._tasks = [Task.from_dict(d) for d in data]
                self._next_id = max((t.id for t in self._tasks), default=0) + 1
        except json.JSONDecodeError:
            print("Error decoding JSON. Starting with an empty task list.")
            self._tasks = []
            self._next_id = 1

    def save_tasks(self):
        data = [t.to_dict() for t in self._tasks]
        with open(self.FILENAME, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
