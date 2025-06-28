import faker
from random import randint, choice
import sqlite3


NUMBER_USERS = 10
NUMBER_TASKS = 30
STATUS = ["new","in progress","completed"]

def generate_fake_data(number_users, number_tasks) -> tuple:
    fake_users = []
    fake_tasks = []
    fake_description = []
    fake_email = []
    fake_data = faker.Faker()

    for _ in range(number_users):
        fake_users.append(fake_data.name())

    for _ in range(number_tasks):
        fake_tasks.append(fake_data.catch_phrase())

    for _ in range(number_users):
        fake_email.append(fake_data.unique.email())

    for _ in range(number_tasks):
        fake_description.append(fake_data.paragraph())
    return fake_users,fake_tasks,fake_description,fake_email


def prepare_data(users, tasks,descriptions,status,email) -> tuple:
    for_users = []
    for user,mail in zip(users,email):
        for_users.append((user,mail))

    for_status = []

    for stat in status:
        for_status.append((stat,))

    for_tasks = []
    for task,description in zip(tasks,descriptions):
        for_tasks.append((task,description,randint(1,len(status)),randint(1,NUMBER_USERS)))

    return for_users,for_tasks,for_status


def insert_data_to_db(users,tasks,status)->None:

    with sqlite3.connect('users_tasks.db')as con:
        cur = con.cursor()

        sql_to_users = """INSERT INTO users(fullname,email) VALUES (?,?)
        """

        sql_to_tasks = """INSERT INTO tasks(title,description,status_id,user_id) VALUES (?,?,?,?)"""


        sql_to_status = """INSERT INTO status(name) VALUES (?)"""

        cur.executemany(sql_to_users,users)
        cur.executemany(sql_to_tasks,tasks)
        cur.executemany(sql_to_status,status)

        con.commit()

if __name__ == "__main__":
    users, tasks,description,email = generate_fake_data(NUMBER_USERS,NUMBER_TASKS)

    print(email)
    users_table,tasks_table,status_table = prepare_data(users,tasks,description,STATUS,email)
    print(users_table)
    insert_data_to_db(users_table,tasks_table,status_table)
