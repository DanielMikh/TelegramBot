# Работа с клавиатурой

from MainDB import MainDB
from telebot import types

class Keyboard(MainDB):
    # Вызов главного меню
    def main_menu(self):
        self.markup = types.ReplyKeyboardMarkup(row_width = 3, resize_keyboard = True)
        button = []
        for curChar in self.load:
            button.append(types.KeyboardButton(curChar))
        self.markup.add(*button)

    #Рекурсивная функция поиска 
    def find(self, message, dictionary):
        for k, v in dictionary.items():
            if k == message:
                yield v
            elif isinstance(v, dict):
                for result in self.find(message, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in self.find(message, d):
                        yield result