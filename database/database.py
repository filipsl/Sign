import sqlite3
from datetime import datetime

def with_connection(func):
    def with_connection_(*args, **kwargs):
        database_path = 'sign.db'
        connection = None
        res = None
        try:
            connection = sqlite3.connect(database_path)
            res = func(connection, *args, **kwargs)
        except sqlite3.DatabaseError as e:
            print(e)
        finally:
            if connection:
                connection.close()
        return res

    return with_connection_


@with_connection
def set_up_database(connection):
    with connection:
        connection.execute("PRAGMA foreign_keys = 1")

        set_up_progress_table(connection)


def set_up_progress_table(connection):
    connection.execute('''CREATE TABLE IF NOT EXISTS Progress
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Date DATETIME,
        Sign TEXT,
        TryCount INTEGER,
        Success INTEGER 
        );''')


@with_connection
def insert_values(connection, table_name, columns, values):
    values = tuple(values)
    columns = tuple(columns)
    command = 'INSERT INTO %s %s values %s ' % (table_name, columns, values)
    print(command)
    with connection:
        connection.execute(command)


@with_connection
def insert_progress(connection, values):
    values = tuple(values)
    command = 'INSERT INTO Progress ("Date", Sign, TryCount, Success) values (?, ?, ?, ?)'
    with connection:
        connection.execute(command, values)


@with_connection
def get_progress_table(connection):
    c = connection.cursor()
    c.execute("SELECT * FROM Progress ORDER BY Date DESC LIMIT 100")
    return c.fetchall()


def get_data():
    data = get_progress_table()
    result = []
    for item in data:
        (id, date, sign, count, success) = item
        d = {
            'id': id,
            'date': date,
            'sign': sign,
            'count': count,
            'success': success
        }
        result.append(d)

    return result