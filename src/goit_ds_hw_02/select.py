import sqlite3


def get_all_tasks_for_user(con,user_id):
    rows = None
    cur = con.cursor()
    sql = """
    SELECT title,description,s.name FROM tasks as t
    JOIN status as s ON s.id = t.status_id
    WHERE t.user_id = ?
    """
    try:
        cur.execute(sql,(user_id,))
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def get_tasks_with_status(con, status):
    rows = None
    cur = con.cursor()
    sql = """
    SELECT title,description,s.name FROM tasks as t
    JOIN status as s ON s.id = t.status_id
    WHERE s.name = ?
    """
    try:
        cur.execute(sql,(status,))
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def update_status_tasks(con,parameters):
    cur = con.cursor()
    sql = """
    UPDATE tasks 
    SET status_id = (
        SELECT id FROM status WHERE name = ?
    )
    WHERE id = ?
    """
    try:
        cur.execute(sql,parameters)
        con.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()


def get_users_without_tasks(con):
    rows = None
    cur = con.cursor()
    sql = """
    SELECT fullname,email FROM users
    WHERE id NOT IN(
    SELECT user_id from tasks
    )
    """
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def add_new_tasks(con,parameters):
    cur = con.cursor()
    sql = """
    INSERT INTO tasks (title,description,status_id,user_id) VALUES (?,?,?,?)
    """
    try:
        cur.execute(sql,parameters)
        con.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()


def get_not_comleted_tasks(con):
    rows = None
    cur = con.cursor()
    sql = """
    SELECT title, description, s.name FROM tasks as t
    JOIN status as s ON t.status_id = s.id
    WHERE s.name != "completed"
    """
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def delete_tasks(con,id):
    cur = con.cursor()
    sql = """
    DELETE FROM tasks WHERE id=?
    """
    try:
        cur.execute(sql,(id,))
        con.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()


def get_users_with_template_email(con,pattern):
    rows = None
    cur = con.cursor()
    sql = """
    SELECT fullname,email FROM users
    WHERE email LIKE ?
    """
    try:
        cur.execute(sql,(pattern,))
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def update_fullname_user(con,parameters):
    cur = con.cursor()
    sql = """
    UPDATE users
    SET fullname = ?
    WHERE fullname = ?
    """
    try:
        cur.execute(sql,parameters)
        con.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()


def get_count_tasks_by_status(con):
    rows = None
    cur = con.cursor()
    sql = """
    SELECT COUNT(t.status_id), s.name FROM tasks as t
    JOIN status as s ON t.status_id = s.id
    GROUP BY t.status_id
    """
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def get_tasks_for_users_by_email_pattern(con,pattern):
    rows = None
    cur = con.cursor()
    sql = """
    SELECT t.title,t.description, u.fullname, u.email FROM tasks as t
    JOIN users as u ON t.user_id = u.id
    WHERE email LIKE ?
    """
    try:
        cur.execute(sql,(pattern,))
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def get_tasks_without_disc(con):
    rows = None
    cur = con.cursor()
    sql = """
    SELECT title FROM tasks
    WHERE description IS NULL
    """
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def get_tasks_in_progress(con):
    rows = None
    cur = con.cursor()
    sql = """
    SELECT u.fullname, t.title, s.name FROM users as u
    JOIN tasks as t ON u.id = t.user_id
    JOIN status as s ON s.id = t.status_id
    WHERE s.name = 'in progress'
    """
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def get_users_count_tasks(con):
    rows = None
    cur = con.cursor()
    sql = """
    SELECT u.fullname, COUNT(t.id)
    FROM users AS u
    LEFT JOIN tasks AS t ON t.user_id = u.id
    GROUP BY u.id
    """
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


if __name__ == "__main__":
    with sqlite3.connect("users_tasks.db") as con:
        rows = get_users_count_tasks(con)
        print(rows)