# Класс для работы с информацией о пользователе
admins = [67413094]

class User():
    def __init__(self, message):
        self.id = message.from_user.id
        self.username = str(message.from_user.first_name)
        self.is_admin = self.id in admins
