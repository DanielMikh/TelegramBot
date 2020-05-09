# Класс для работы с основной базой данных

import json

class MainDB():
    def __init__(self):
        with open('new_db.json','r') as data:
            self.load = json.load(data)

            # self.dump = json.dumps([*self.load], ensure_ascii = False)

    def get_dump(self):
        self.dump = json.dumps([*self.load], ensure_ascii = False)
        return self.dump
    
    # data - словарь после изменений через /admin
    def save_db(self, data):
        with open('new_db.json', 'w+') as db:
            json.dump(data, db, ensure_ascii = False)

                        