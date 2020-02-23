import telebot
from telebot import types
import json
import random
from config import TOKEN, msg, msg1, photo

from User import User
from UserDB import UserDB

bot = telebot.TeleBot(TOKEN)

user_db = UserDB()

def load_maindb():
    with open('testdb.json', 'r') as basa:
        global db
        db = json.load(basa)

def main_menu():
    global markup
    markup = types.ReplyKeyboardMarkup(row_width = 3, resize_keyboard = True)
    button = []
    for curChar in db:
        button.append(types.KeyboardButton(curChar))
    markup.add(*button)

@bot.message_handler(commands = ['start'])
def send_start(message):
    load_maindb()

    user = User(message)

    main_menu()

    if user.id in user_db.users:
        bot.send_photo(user.id, random.choice(photo))
        bot.send_message(user.id, random.choice(msg1).format(name = user.username), reply_markup = markup)
    else: 
        bot.send_photo(user.id, random.choice(photo))
        bot.send_message(user.id, random.choice(msg).format(name = user.username), reply_markup = markup)

        user_db.save_user(user.id)

@bot.message_handler(func=lambda message: True)
def button_selection(message):
    global db
    global markup
    if db[message.text]:
        markup = types.ReplyKeyboardMarkup(row_width = 3, resize_keyboard = True)
        button = []
        for curChar in db[message.text]:
            if curChar == 'text_msg':
                text = curChar
            elif curChar == 'photo_msg':
                pass
            else:
                button.append(types.KeyboardButton(curChar))
        markup.add(*button)
        db = db[message.text]
        try:
            bot.send_message(message.from_user.id, db[text], reply_markup = markup)
        except KeyError:
            pass
        # try:
        #     bot.send_photo(message.from_user.id, db[photo])
        # except KeyError:
        #     pass
        return db
    elif message.text == 'На главную':
        load_maindb()
        main_menu()
        bot.reply_to(message, "Хорошо", reply_markup = markup)


if __name__ == "__main__":
    bot.infinity_polling()



