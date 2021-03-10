from time import sleep
from datetime import datetime


from scheduler.enums import Tasks


schedules = {
    Tasks.PULL_REQUESTS: 60,
    Tasks.ORG_SCAN: 120,
}

executed = {
    Tasks.PULL_REQUESTS: None,
    Tasks.ORG_SCAN: None,
}


def refresh(task) -> bool:
    dt = executed.get(task)
    if not dt or (datetime.now() - dt).seconds > schedules.get(task):
        executed[task] = datetime.now()
        return True
    return False


def update():
    while True:
        for task in schedules:
            refreshed = refresh(task)
            print(f"refresh task {task.id} {refreshed}")
        sleep(1)
