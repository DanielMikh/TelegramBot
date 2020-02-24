# Класс для работы с информацией о пользователе

class User():
    def __init__(self, message):
        self.id = message.from_user.id
        self.username = str(message.from_user.first_name)
