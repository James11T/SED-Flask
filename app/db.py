import sqlite3
import bcrypt
import os

env = os.getenv("ENV", "dev")

database_uri = ":memory:" if env == "test" else "mydb.sqlite"

connection = sqlite3.connect(database_uri, check_same_thread=False)

def create_tables():
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user
                (id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL)''')

    connection.commit()

def create_user(username, password):
    encoded_password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())

    cursor = connection.cursor()
    cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, hashed_password))

    connection.commit()

    return cursor.lastrowid

def check_password(username, password):
    cursor = connection.cursor()

    cursor.execute("SELECT password FROM user WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result:
        hashed_password = result[0]

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return True
        else:
            return False
    else:
        return False


def get_users():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user")

    all_users = cursor.fetchall()

    return all_users