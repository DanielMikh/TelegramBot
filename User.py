class User():
    def __init__(self, message):
        self.id = message.from_user.id
        self.username = str(message.from_user.username)
    
    def get_commit(self):
        pass