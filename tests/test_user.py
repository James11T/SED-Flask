from app.db import create_user, get_users, check_password

def test_create_user():
    user_id = create_user("test_user", "mypassword")

    assert(type(user_id) == int) # Check create user returns new user id
    assert(len(get_users()) == 1) # Check user is actually in the database

def test_check_password():
    success = check_password("test_user", "mypassword")

    assert(success) # Check correct password

    success = check_password("test_user", "wrongpassword")

    assert(not success) # Check wrong password