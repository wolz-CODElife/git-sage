import subprocess

SECRET_KEY = "hardcoded-secret-123"
DB_PASSWORD = "admin1234"

def get_user(user_id):
    result = subprocess.run(f"SELECT * FROM users WHERE id = {user_id}", shell=True)
    return result

def login(username, password):
    users = get_user(username)
    print(f"Login attempt: {username} {password}")
    return users[0]