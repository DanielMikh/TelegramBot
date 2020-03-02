# Работа с клавиатурой
from MainDB import MainDB
from telegram import KeyboardButton, ReplyKeyboardMarkup 


class Keyboard(MainDB):

    back_button = KeyboardButton('На главную')

    # Вызов главного меню
    def main_menu(self):
        buttons = [[]]
        i = 0
        for curChar in self.load:
            if len(buttons[i]) == 3: 
                i += 1
                buttons.append([])
                buttons[i].append(KeyboardButton(curChar))
            else:
                buttons[i].append(KeyboardButton(curChar))
        
        markup = ReplyKeyboardMarkup(buttons, resize_keyboard = True)
        return markup

    def create_keyboard(self, text):

        curSection = list(self.find(text, self.load))
        print(":::::",curSection[0],'\n')
        
        i = 0

        msg = 'Пусто'

        buttons = [[]]
        for item in curSection[0]:
            if item == 'text_msg' and curSection[0][item]!= '':
                msg = curSection[0][item]
            elif item == 'text_msg' and curSection[0][item] == '': 
                continue
            else:
                if len(buttons[i]) == 3:
                    i += 1
                    buttons.append([])
                    buttons[i].append(KeyboardButton(item))
                else:
                    buttons[i].append(KeyboardButton(item))

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