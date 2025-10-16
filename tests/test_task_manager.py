import json
from pathlib import Path
import pytest

from task_manager import TaskManager, Task


def test_add_and_list_and_persist(tmp_path, capsys):
    temp_file = tmp_path / "tasks.json"
    TaskManager.FILENAME = str(temp_file)

    mgr = TaskManager()
    mgr.delete_all_tasks()

    mgr.add_task("Tarea uno")
    mgr.add_task("Tarea dos")

    # Capture printed list
    mgr.list_tasks()
    captured = capsys.readouterr()
    assert "Tarea uno" in captured.out
    assert "Tarea dos" in captured.out

    # Check persisted file
    data = json.loads(temp_file.read_text(encoding="utf-8"))
    assert len(data) == 2
    assert data[0]["description"] == "Tarea uno"


def test_complete_task_updates_state_and_file(tmp_path, capsys):
    temp_file = tmp_path / "tasks.json"
    TaskManager.FILENAME = str(temp_file)

    mgr = TaskManager()
    mgr.delete_all_tasks()

    mgr.add_task("Completar texto")
    mgr.complete_task(1)
    captured = capsys.readouterr()
    assert "Task completed" in captured.out

    data = json.loads(temp_file.read_text(encoding="utf-8"))
    assert data[0]["completed"] is True


def test_delete_task_existing_and_nonexisting(tmp_path, capsys):
    temp_file = tmp_path / "tasks.json"
    TaskManager.FILENAME = str(temp_file)

    mgr = TaskManager()
    mgr.delete_all_tasks()

    mgr.add_task("A")
    mgr.add_task("B")

    mgr.delete_task(1)
    captured = capsys.readouterr()
    assert "Task deleted" in captured.out

    # delete non-existing
    mgr.delete_task(999)
    captured = capsys.readouterr()
    assert "No task found with ID: 999" in captured.out


def test_delete_all_tasks_clears_file(tmp_path):
    temp_file = tmp_path / "tasks.json"
    TaskManager.FILENAME = str(temp_file)

    mgr = TaskManager()
    mgr.delete_all_tasks()

    mgr.add_task("X")
    mgr.add_task("Y")

    mgr.delete_all_tasks()

    assert temp_file.exists()
    data = json.loads(temp_file.read_text(encoding="utf-8"))
    assert data == []
