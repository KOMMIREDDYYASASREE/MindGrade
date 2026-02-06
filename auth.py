import json

def authenticate(username, password):
    with open("data/users.json") as f:
        users = json.load(f)

    if username in users and users[username]["password"] == password:
        return users[username]["role"]
    return None
