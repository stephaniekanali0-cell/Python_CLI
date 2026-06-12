import argparse
from rich.console import Console
from rich.table import Table


from Models.Project import Project
from Models.Task import Task
from Models.User import User
from Utils.file_handler import load_data,save_data

console= Console()    
DATA_FILE = "Data/Users.json"


def load_users():
    raw_data = load_data(DATA_FILE)
    users = []
    for item in raw_data:
        new_user = User(name=item['name'], email=item['email'])
        for project_data in item.get('projects', []):
            project = Project(title=project_data['title'], description=project_data['description'], due_date=project_data['due_date'])
            for task_data in project_data.get('tasks',[]):
                task = Task(title=task_data['title'], description=task_data['description'], completed=task_data['completed'])
                project.add_task(task)
            new_user.add_projects(project)
        users.append(new_user)
    return users

def save_users(users):
    save_data(DATA_FILE, [user.to_dict() for user in users])

def find_user(users,name):
    for user in users:
        if user.name.lower() == name.lower():
            return user
    return None

def find_project(users,title):
    for project in users.projects:
        if project.title.lower() == title.lower():
            return project
    return None,None

def cmd_add_user(args):
    users= load_users()
    if find_user(users,args.name):
        console.print(f"[red]User wit name {args.name} already exists. [/red]")
        return
    new_user = User(name = args.name, email = args.email)
    users.append(new_user)
    save_users(users)
    console.print(f"[green]user {args.name} added successfully. [/green]")

def cmd_list_users(args):
    users = load_users()
    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return
    table = Table(title = "Users")
    table.add_column("Name", style="cyan")
    table.add_column("Email", style="magenta")
    for user in users:
        table.add_row(user.name, user.email)
    console.print(table)

def cmd_add_project(args):
    users = load_users()
    user = find_user(users, args.user)
    if not user:
        console.print(f"[red]User '{args.user}' not found.[/red]")
        return
    user.add_projects(Project(args.title,args.description,args.due_date))
    save_users(users)
    console.print(f"[green]Project '{args.title}' added to {args.user}.[/green]")

def cmd_list_projects(args):
    users = load_users()
    user = find_user(users, args.user)
    if not user:
        console.print(f"[red]User '{args.user}' not found.[/red]")
        return
    if not user.projects:
        console.print(f"[yellow]{args.user} has no projects yet.[/yellow]")
        return
    table = Table(title=f"Projects for {user.name}")
    table.add_column("Title", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Due Date", style="yellow")
    table.add_column("Tasks", style="green")
    for p in user.projects:
        table.add_row(p.title, p.description, p.due_date, str(len(p.tasks)))
    console.print(table)

def cmd_add_task(args):
    users = load_users()
    _, project = find_project(users, args.project)
    if not project:
        console.print(f"[red]Project '{args.project}' not found.[/red]")
        return
    project.add_task(Task(args.title, args.assigned_to))
    save_users(users)
    console.print(f"[green]Task '{args.title}' added to project '{args.project}'.[/green]")

def cmd_complete_task(args):
    users = load_users()
    _, project = find_project(users, args.project)
    if not project:
        console.print(f"[red]Project '{args.project}' not found.[/red]")
        return
    for task in project.tasks:
        if task.title.lower() == args.title.lower():
            task.complete()
            save_users(users)
            console.print(f"[green]Task '{args.title}' marked as Completed.[/green]")
            return
    console.print(f"[red]Task '{args.title}' not found.[/red]")


def main():
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    p_add_user = subparsers.add_parser("add-user", help="Add a new user")
    p_add_user.add_argument("--name", required=True)
    p_add_user.add_argument("--email", required=True)
    p_add_user.set_defaults(func=cmd_add_user)

    p_list_users = subparsers.add_parser("list-users", help="List all users")
    p_list_users.set_defaults(func=cmd_list_users)

    p_add_proj = subparsers.add_parser("add-project", help="Add a project to a user")
    p_add_proj.add_argument("--user", required=True)
    p_add_proj.add_argument("--title", required=True)
    p_add_proj.add_argument("--description", default="")
    p_add_proj.add_argument("--due-date", dest="due_date", required=True)
    p_add_proj.set_defaults(func=cmd_add_project)

    p_list_proj = subparsers.add_parser("list-projects", help="List projects for a user")
    p_list_proj.add_argument("--user", required=True)
    p_list_proj.set_defaults(func=cmd_list_projects)

    p_add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    p_add_task.add_argument("--project", required=True)
    p_add_task.add_argument("--title", required=True)
    p_add_task.add_argument("--assigned-to", dest="assigned_to", required=True)
    p_add_task.set_defaults(func=cmd_add_task)

    p_complete = subparsers.add_parser("complete-task", help="Mark a task as complete")
    p_complete.add_argument("--project", required=True)
    p_complete.add_argument("--title", required=True)
    p_complete.set_defaults(func=cmd_complete_task)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()