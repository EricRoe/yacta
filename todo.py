'''todo

Usage:
  todo
  todo edit <task_id> ... [--priority <priority>] [--tags <tags>]
  todo add <task> [--priority <priority>] [--tags <tags>]
  todo rm <task_id> ...
  todo filter <tags_match> ...

Options:
  -p <priority>, --priority <priority> Set the priority, sorted lexically in
                                           reverse order.  Recommended to use only 0-9
  -t <tags>, --tags <tags>             Set the tags.  Filter searches this 
                                           string for each item in <tags_match>

  -h --help                            Show this text

'''

from docopt import docopt
from task import Task
import pickle
import os

store = os.path.dirname(os.path.realpath(__file__)) + './store.txt'

def main():
    args = docopt(__doc__)

    # print(args)

    if args['add']: 
        add(args)
    elif args['rm']: 
        rm(args)
    elif args['edit']: 
        edit(args)
    elif args['filter']:
        filter_(args)
    else: 
        print_all()


def filter_(args):
    tasks = [t for t in load_tasks() if any(s_m in t.tags for s_m in args['<tags_match>'])]
    tasks.sort(key=lambda t: t.priority, reverse=True)
    print(table_ify(tasks, 1))


def rm(args):
    tasks = [t for t in load_tasks() if t.id not in args['<task_id>']]
    save_tasks(tasks)


def edit(args):
    tasks = load_tasks()

    for t in tasks:
        if t.id in args['<task_id>']:
            t.tags = args['--tags'] or t.tags
            t.priority = args['--priority'] or t.priority

    save_tasks(tasks)


def add(args):
    tasks = load_tasks()

    id_candidate = 0
    used_ids = [t.id for t in tasks]
    while str(id_candidate) in used_ids:
        id_candidate += 1
    
    tasks.append(Task(args['<task>'], args['--tags'] or '-', args['--priority'] or '0', str(id_candidate)))
    save_tasks(tasks)


def print_all():
    tasks = load_tasks()
    if not tasks:
        print("No tasks. Add with 'todo add <task>'")
        return
    tasks.sort(key=lambda t: t.priority, reverse=True)
    print(table_ify(tasks, 3))


def load_tasks():
    try:
        with open(store, 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []


def save_tasks(tasks):
    try:
        with open(store, 'wb') as f:
            pickle.dump(tasks, f)
    except Exception as e:
        print("The following error occured while attempting to save your data.")
        print("Changes may not have been saved.")
        print()
        print(e)


def make_row(start, lengths, fill_char, section_endings, end='\n'):
    row = start
    for length, ending in zip(lengths, section_endings):
        row += ''.ljust(length, fill_char) + ending
    return row + end


def table_ify(tasks, divide_every=0):
    # there should be a more elegant method than using lambdas
    getters = [lambda t:t.id, lambda t:t.text, lambda t:t.tags, lambda t:t.priority]
    labels = ['ID', 'Task', 'Tags', 'Priority']
    lengths = [max(max(len(getter(t)) for t in tasks), len(label)) for getter, label in zip(getters, labels)]
    table  = '\n\n'
    
    # top boarder
    table += make_row('╔', lengths, '═', ['╤', '╤', '╤', '╗'])
    
    # column labels
    table += '║'
    for label, length, ending in zip(labels, lengths, ['│', '│', '│', '║\n']):
        table += label.center(length) + ending
    
    # label/item separator
    table += make_row('╠', lengths, '═', ['╪', '╪', '╪', '╣'])
    
    # task entries
    for index, task in enumerate(tasks, start=1):
        table += '║'
        for getter, length, ending in zip(getters, lengths, ['│', '│', '│', '║\n']):
            table += getter(task).ljust(length) + ending
        # divider for readability
        if divide_every and not (index % divide_every) and len(tasks) != index:
            table += make_row('╟', lengths, '─', ['┼', '┼', '┼', '╢'])
            
    # bottom boarder
    table += make_row('╚', lengths, '═', ['╧', '╧', '╧', '╝\n'])
    
    return table


if __name__ == '__main__':
    main()