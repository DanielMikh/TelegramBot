# Класс для работы с основной базой данных

import json

class MainDB():
    def __init__(self):
        with open('testdb.py','r') as data:
            self.load = json.load(data)