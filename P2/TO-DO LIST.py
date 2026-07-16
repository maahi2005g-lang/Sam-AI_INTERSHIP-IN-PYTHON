from termcolor import colored
import json

print(colored("Hello this is your to_do_list", "blue", attrs=["bold"]))
print(colored("Commands: add, delete, show, exit\n", "green"))

tasks = []

try:
    with open("tasks.json") as jsonfile:
        tasks = json.load(jsonfile)
except (FileNotFoundError, json.JSONDecodeError):
    tasks = []

def add(title, priority):
    task = {
        "title": title,
        "priority": priority, 
        "done": False
    }
    tasks.append(task)
def delete(index):
    tasks.pop(int(index) - 1)
def show():
    if tasks == []:
        print("You don`t have anything in your to_do_list")
    for index, task in enumerate(tasks, start=1):
        if task["done"]:
            done = "✔"
        else:
            done = "✘"    
        print(f"{index}. {done} {task['title']} (Priority: {task['priority']})")
def save():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)
def done(index):
    tasks[int(index)-1]["done"] = True

while True:  
    user = input("> ")

    if user == "show":
        show()
    elif user == "add":
        add(input("What you want to add > "), input("Set priority > "))
        save()
    elif user == "delete":
        delete(input("What you want to delete > "))
        save()
    elif user == "exit":
        break
    else:
        print(colored("Unknown command", "red"))
