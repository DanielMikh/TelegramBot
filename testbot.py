import telebot
from telebot import types
import random
from config import TOKEN, msg, msg1, photo

from MainDB import MainDB
from User import User
from UserDB import UserDB
from Keyboard import Keyboard

bot = telebot.TeleBot(TOKEN)

user_db = UserDB()
main_db = MainDB()
keyboard = Keyboard()

@bot.message_handler(commands = ['start'])
def send_start(message):

    user = User(message)

    keyboard.main_menu()

    if user.id in user_db.users:
        bot.send_photo(user.id, random.choice(photo))
        bot.send_message(user.id, random.choice(msg1).format(name = user.username), reply_markup = keyboard.markup)
    else: 
        bot.send_photo(user.id, random.choice(photo))
        bot.send_message(user.id, random.choice(msg).format(name = user.username), reply_markup = keyboard.markup)

        user_db.save_user(user.id)

@bot.message_handler(func = lambda message: message.text == 'На главную') 
def return_to_main_menu(message):   
    keyboard.main_menu()
    bot.send_message(message.from_user.id, 'Хорошо, сделано.', reply_markup = keyboard.markup)

@bot.message_handler(func=lambda message: True)
def button_selection(message):
    markup = types.ReplyKeyboardMarkup(row_width = 3, resize_keyboard = True)
    button = []

    curSection = list(keyboard.find(message.text, main_db.load))
        
    for item in curSection[0]:
        if item == 'text_msg':
            msg = curSection[0][item]
        else:
            button.append(types.KeyboardButton(item))
    markup.add(*button)
    bot.send_message(message.from_user.id, msg, reply_markup = markup)

if __name__ == "__main__":
    bot.infinity_polling()



