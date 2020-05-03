# Класс для работы с базой данных пользователей
from User import User
import json

class UserDB(User):
    # users: List<UserID>

    def __init__(self):
        with open('iddb.json', 'r') as db:
            self.users = json.load(db)
            print(":READ:", self.users)

    def save_user(self, user_id):
        with open('iddb.json', 'w+') as db:
            self.users.append(user_id)
            print(":WRITE:", self.users)
            json.dump(self.users, db, ensure_ascii=False)
