import argparse

def add_task(args):
    print('adding task...')
    print(f'task description {args.description}')

def delete_task(args):
    print('removing task...')
    print(f'task id to remove {args.id}')

def update_task(args):
    print('updating task...')
    print(f'task id to update {args.id}')


def main():
    parser = argparse.ArgumentParser(
        prog="task-tracker",
        description="Task Tracker application",
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command", required=True, help="Available Commands")

    # Add command
    parser_add = subparsers.add_parser("add", help="Adds a new task.")
    parser_add.add_argument("description", type=str, help="Task description.")
    parser_add.set_defaults(func=add_task)

    # Delete command
    parser_add = subparsers.add_parser("delete", help="Removes a task.")
    parser_add.add_argument("id", type=int, help="Task id.")
    parser_add.set_defaults(func=delete_task)
    
    # Update command
    parser_add = subparsers.add_parser("update", help="Updates a task.")
    parser_add.add_argument("id", type=int, help="Task id.")
    parser_add.set_defaults(func=update_task)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args) # Pasamos las tareas cargadas a la función del comando
    else:
        parser.print_help() # Si no se proporciona un subcomando válido

if __name__ == '__main__':
    main()