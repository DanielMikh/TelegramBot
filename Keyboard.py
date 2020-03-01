# Работа с клавиатурой

from MainDB import MainDB
from telebot import types

class Keyboard(MainDB):

    back_button = types.KeyboardButton('На главную')

    # Вызов главного меню
    def main_menu(self, for_admin = False):
        markup = types.ReplyKeyboardMarkup(row_width = 3, resize_keyboard = True)
        button = []
        for curChar in self.load:
            button.append(types.KeyboardButton(curChar))

        if for_admin:
            button.append(types.KeyboardButton('Добавить раздел'))

        markup.add(*button)
        return markup

    def create_keyboard(self, text, for_admin = False):

        markup = types.ReplyKeyboardMarkup(row_width = 3, resize_keyboard = True)

        curSection = list(self.find(text, self.load))
        print(curSection)

        msg = 'Пусто'
        button = []
        for item in curSection[0]:
            if item == 'text_msg':
                if curSection[0][item] != '':
                    msg = curSection[0][item]
                else: pass
            else:
                button.append(types.KeyboardButton(item))

        if for_admin:
            button.append(types.KeyboardButton('Добавить раздел'))
            button.append(types.KeyboardButton('Изменить описание'))
            button.append(types.KeyboardButton('Удалить раздел'))

        markup.add(*button)
        markup.add(self.back_button)

        return msg, markup

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