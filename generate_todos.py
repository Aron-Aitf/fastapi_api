from json import load, dump

from faker import Faker
from random import choice

NUM_FAKE_TODOS_TITLES = 2 ^ 8
NUM_TODOS_TO_GENERATE = NUM_FAKE_TODOS_TITLES * 200

faker = Faker()

todo_titles = []

fake_todos: list[dict[str, str | bool | None]] = []

with open("./data/todos.json", "r") as file:
    todo_titles: list[str] = load(file)

for i in range(NUM_TODOS_TO_GENERATE):
    fake_todo = {}
    fake_todo["title"] = todo_titles[i % NUM_FAKE_TODOS_TITLES]

    if choice([0, 1, 2, 3, 4]) != 0:
        fake_todo["description"] = faker.sentence(variable_nb_words=True, nb_words=7)
    else:
        fake_todo["description"] = None

    fake_todo["is_competed"] = choice([True, False, False])

    if choice([0, 1, 2, 3, 4]) != 0:
        fake_todo["completion_date"] = faker.date_time_this_month(
            before_now=False, after_now=True
        ).isoformat()
    else:
        fake_todo["completion_date"] = None

    fake_todos.append(fake_todo)

with open("data/todo_list.json", "w") as file:
    dump(fake_todos, file, indent=4)
