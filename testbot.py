from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)
import random
from config import TOKEN, msg, msg1, photo

from MainDB import MainDB
from User import User
from UserDB import UserDB
from Keyboard import Keyboard

user_db = UserDB()
main_db = MainDB()
keyboard = Keyboard()

# def send_admin(update, context):


def send_start(update, context):

    user = User(update.message)

    if user.id in user_db.users:
        context.bot.send_photo(user.id, random.choice(photo))
        context.bot.send_message(chat_id = user.id, text = random.choice(msg).format(name = user.username), reply_markup = keyboard.main_menu())
    else: 
        context.bot.send_photo(user.id, random.choice(photo))
        context.bot.send_message(user.id, random.choice(msg1).format(name = user.username), reply_markup = keyboard.main_menu())

        user_db.save_user(user.id)

def return_to_main_menu(update, context):  
    user = User(update.message) 
    keyboard.main_menu()
    context.bot.send_message(user.id, 'Хорошо, сделано.', reply_markup = keyboard.main_menu())


def button_selection(update, context):
    user = User(update.message)

    msg, markup = keyboard.create_keyboard(update.message.text)
    
    context.bot.send_message(user.id, msg, reply_markup = markup)

def main():
    updater = Updater(token = TOKEN, use_context = True)
    dp = updater.dispatcher

    start_handler = CommandHandler('start', send_start)
    msg_handler1 = MessageHandler(Filters.regex('На главную'), return_to_main_menu)
    msg_handler2 = MessageHandler(Filters.text, button_selection)

    dp.add_handler(start_handler)
    dp.add_handler(msg_handler1)
    dp.add_handler(msg_handler2)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()