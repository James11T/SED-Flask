import sqlite3
import bcrypt
import os

env = os.getenv("ENV", "dev")

# If the ENV environment variable is set to "test" then use a new "in memory" database
# This means that a database does not need to be committed to the repository
# It also helps improve the isolation of the tests as no existing data can be in an "in-memory" database
database_uri = ":memory:" if env == "test" else "mydb.sqlite"

connection = sqlite3.connect(database_uri, check_same_thread=False)

"""
Create all the tables in the database if they do not exist
"""
def create_tables():
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user
                (id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL)''')

    connection.commit()


"""
Hash a users password and store them in the database
"""
def create_user(username, password):
    encoded_password = password.encode('utf-8') # Ensure the password is in Unicode / UTF-8
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())

    cursor = connection.cursor()
    # Insert into the database
    cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, hashed_password))

    # Save changes
    connection.commit()
    
    # Return new user ID
    return cursor.lastrowid


"""
Checks a users username and password
Returns True if the username and password are found and correct
Returns False if either the username doesn't exist or the password is incorrect
"""
def check_password(username, password):
    cursor = connection.cursor()

    # Select only the password
    cursor.execute("SELECT password FROM user WHERE username = ?", (username,))

    # Select the first instance of the password
    result = cursor.fetchone()

    # Check username matched
    if not result: return False

    hashed_password = result[0]

    # Use bcrypt to check the password against the hash in the database
    # bcrypt.checkpw always returns True or False so the result can be directly returned
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


"""
Return a list of all the users in the database
"""
def get_users():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user")

    # Select all responses
    all_users = cursor.fetchall()

    return all_users