import json
from pathlib import Path
from task import Task

DATA_FILE = "tasks.json"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.index = 1

        if Path(DATA_FILE).is_file():
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.tasks = [Task(**t) for t in data]

            if self.tasks:
                self.index = max(t.num for t in self.tasks) + 1

    def save(self):
        tasks_data = [t.to_dict() for t in self.tasks]
        with open(DATA_FILE, "w") as f:
            json.dump(tasks_data, f, indent=2)

    def add(self, title, status):
        self.tasks.append(Task(self.index, title, status))
        self.index += 1

    def delete(self, num, status, ranges):
        if ranges is not None:
            items : list[Task] = self.find_range(ranges)
            if status is not None:
                f_items = [t for t in items if t.status == status]
                for item in f_items:
                    self.tasks.remove(item)
            else:
                for item in items:
                    self.tasks.remove(item)

        elif status is not None:
            items = [t for t in self.tasks if t.status == status]
            for item in items:
                self.tasks.remove(item)
        elif num:
            item = self.find(num)
            if item is not None:
                self.tasks.remove(item)

    def update(self, num, status, ranges, status_from):
        if ranges is not None:
            items: list[Task] = self.find_range(ranges)
            if status is not None:
                f_items = [t for t in items if t.status == status_from]
                for item in f_items:
                    item.status = status
            else:
                for item in items:
                    item.status = status

        elif status_from is not None:
            items = [t for t in self.tasks if t.status == status_from]
            for item in items:
                item.status = status
        elif num:
            item = self.find(num)
            if item is not None:
                item.status = status

    def list(self, status, ranges):
        if ranges is not None:
            items = [t for t in self.tasks if t.num in ranges]
            if status is not None:
                items = [t for t in items if t.status == status]
                if len(items) == 0:
                    print("Empty")
                else:
                    for t in items:
                        t.print()

        elif status is not None:
            items = [t for t in self.tasks if t.status == status]
            if len(items) == 0:
                print("Empty")
            else:
                for t in items:
                    t.print()
        else:
            if len(self.tasks) == 0:
                print("Empty")
            else:
                for t in self.tasks:
                    t.print()



    def find(self, num):
        return next((t for t in self.tasks if t.num == num), None)

    def find_range(self, range_nums):
        items = [t for t in self.tasks if t.num in range_nums]
        return items