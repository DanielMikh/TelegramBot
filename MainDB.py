# Класс для работы с основной базой данных

import json

class MainDB():
    def __init__(self):
        with open('new_db.json','r') as data:
            self.load = json.load(data)
    

                        