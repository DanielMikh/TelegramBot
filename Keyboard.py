# Работа с клавиатурой
from MainDB import MainDB
from telegram import KeyboardButton, ReplyKeyboardMarkup 


class Keyboard(MainDB):

    back_button = KeyboardButton('На главную')
    section_back_button = KeyboardButton('Назад')
    def __init__(self):
        super().__init__()
        self.user_path_section = {}

    def add_user_section(self, user_id, section):
        if user_id not in self.user_path_section:
            self.user_path_section[user_id] = []

        self.user_path_section[user_id].append(section)

    def clear(self, user_id):
        self.user_path_section[user_id].clear()

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

    def create_keyboard(self, text, user_id):
        curSection = list(self.find(text, self.load))
        
        i = 0
        msg = ''

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

        if len(self.user_path_section[user_id]) > 1:
            buttons.append([self.section_back_button])

        buttons.append([self.back_button])
        
        markup = ReplyKeyboardMarkup(buttons, resize_keyboard = True)
        return msg, markup
