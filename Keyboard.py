# Работа с клавиатурой

from MainDB import MainDB
from telegram import KeyboardButton, ReplyMarkup, ReplyKeyboardMarkup 
from telegram.ext import Updater

class Keyboard(MainDB):

    back_button = KeyboardButton('На главную')

    # Вызов главного меню
    def main_menu(self, for_admin = False):
        first_buttons_row = []
        admin_buttons_row = []
        buttons = [first_buttons_row, admin_buttons_row]
        for curChar in self.load:
            first_buttons_row.append(KeyboardButton(curChar))

        if for_admin:
            admin_buttons_row.append(KeyboardButton('Добавить раздел'))

        markup = ReplyKeyboardMarkup(buttons, resize_keyboard = True)
        return markup

    def create_keyboard(self, text, for_admin = False):

        curSection = list(self.find(text, self.load))
        print(":::::",curSection[0],'\n')
        
        msg = 'Пусто'
        buttons = []
        for item in curSection[0]:
            if item == 'text_msg':
                if curSection[0][item] != '':
                    msg = curSection[0][item]
                else: continue
            else:
                buttons.append([KeyboardButton(item)])

        if for_admin:
            buttons.append([KeyboardButton('Добавить раздел')])
            buttons.append([KeyboardButton('Изменить описание')])
            buttons.append([KeyboardButton('Удалить раздел')])

        buttons.append([self.back_button])
        markup = ReplyKeyboardMarkup(buttons, resize_keyboard = True)
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