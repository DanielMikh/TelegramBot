from telegram import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

import random

from config import TOKEN, msg, msg1, photo, main_msg_inuserbd, main_msg_notinuserdb
from MainDB import MainDB
from User import User
from UserDB import UserDB
from Keyboard import Keyboard

from Admin import Admin

user_db = UserDB()
main_db = MainDB()
keyboard = Keyboard()
admin = Admin()

user_last_section = {}

SELECTING_ACTION, ADDING_SECTION, EDIT_SECTION, CURRENT_FEATURE, TYPING, FEATURES = range(6)

# Конец диалога /admin
END = ConversationHandler.END

"""Администрирование"""
def start_admin(update, context):
    user = User(update.message)
    if not user.is_admin:
        context.bot.send_message(chat_id = user.id, text = 'У вас нет прав.')
        return
    
    """Выберите действие: Создать/отредактировать раздел"""
    buttons = [[
        InlineKeyboardButton(text = 'Создать', callback_data = str(ADDING_SECTION)),
        InlineKeyboardButton(text = 'Отредактировать', callback_data = str(EDIT_SECTION))
    ], [
        InlineKeyboardButton(text='Выход из панели', callback_data = str(END))
    ]]
    kkeyboard = InlineKeyboardMarkup(buttons)

    update.message.reply_text('У администратора есть возможность добавлять разделы и их контекст. '\
            'Вы видите список разделов и наличие text_msg. При наличии можно отредактировать.')

    sections = []
    try:
        currentSection = user_last_section[user.id]
        print("try user_last_section: ", user_last_section)
        section = keyboard.find(currentSection, main_db.load)
        sec = list(section)[0]
        sect = list(sec.keys())
        sections = admin.list_to_str(sect)
        print("::::SECTIONS", sections)
        keyboard.create_keyboard(currentSection, user.id)
    except KeyError:
        print("except user_last_section: ", user_last_section)
        sections = main_db.get_dump()
        ReplyKeyboardMarkup(keyboard.main_menu())

    update.message.reply_text(text = sections, reply_markup = kkeyboard)

    return SELECTING_ACTION
    

def create_section(update, context):
    user = User(update.message)
    new_section_name = context.user_data["text"]

    try:
        currentSection = user_last_section[user.id]
        section = keyboard.find(currentSection, main_db.load)
        list(section)[0][new_section_name] = { 'text_msg': 'Пусто' }
    except KeyError:
        main_db.load[new_section_name] = { 'text_msg': 'Пусто' }

    keyboard.load = main_db.load
    main_db.save_db(main_db.load)
    

def edit_section(update, context):
    user = User(update.message)
    currentSection = user_last_section[user.id]
    print("::::curSect", currentSection)

    new_section_text = update.message.text

    print("::::new_section_text", update.message.text)

    if currentSection is None:
        return
    else:
        section = keyboard.find(currentSection, main_db.load)
        list(section)[0]['text_msg'] = new_section_text

    keyboard.load = main_db.load
    main_db.save_db(main_db.load)


def ask_for_input(update, context):
    """Переход после выбора: создать раздел/редактировать/выйти из панели"""
    name_text = 'Отлично, напишите название нового раздела.'
    context_text = 'Хорошо, какую информацию будет присылать раздел? Напишите.'
    
    context.user_data["func"] = update.callback_query.data
    update.callback_query.answer()

    if context.user_data["func"] == str(ADDING_SECTION):
        update.callback_query.edit_message_text(text = name_text)
        return TYPING
    elif context.user_data["func"] == str(EDIT_SECTION):
        update.callback_query.edit_message_text(text = context_text)
        return TYPING
    elif context.user_data["func"] == str(END):
        print(":::END")
        cancel(update, context)


def save_input(update, context):
    """Save input for feature and return to feature selection."""
    
    context.user_data["text"] = update.message.text

    if context.user_data["func"] == str(ADDING_SECTION):
        create_section(update, context)
    elif context.user_data["func"] == str(EDIT_SECTION):
        edit_section(update, context)

    return start_admin(update, context)

def cancel(update, context):
    print(":::::CANCEL")
    query = update.callback_query
    query.answer()
    query.edit_message_text(text = "На этом закончили изменения!")


"""Работа с пользователем"""
def send_start(update, context):
    user = User(update.message)

    if user.id in user_db.users:
        context.bot.send_photo(chat_id = user.id, photo = random.choice(photo))
        context.bot.send_message(chat_id = user.id, text = random.choice(msg).format(name = user.username), reply_markup = keyboard.main_menu())
        context.bot.send_message(chat_id = user.id, text = main_msg_inuserbd)
        
        if user.is_admin:
            context.bot.send_message(parse_mode = 'HTML', chat_id = user.id, text = 'У вас есть <b><i>права</i></b> администратора, введите команду /admin, чтобы внести изменения.')
    else: 
        context.bot.send_photo(chat_id = user.id, photo = random.choice(photo))
        context.bot.send_message(chat_id = user.id, text = random.choice(msg1).format(name = user.username), reply_markup = keyboard.main_menu())

        context.bot.send_message(chat_id = user.id, text = main_msg_notinuserdb)

        user_db.save_user(user.id)
    

def return_to_main_menu(update, context):  
    user = User(update.message) 

    keyboard.main_menu()

    context.bot.send_message(chat_id = user.id, text = 'Вернемся на главную.', reply_markup = keyboard.main_menu())

    keyboard.clear(user_id = user.id)

    del user_last_section[user.id] 
    return user_last_section 


def button_selection(update, context):
    user = User(update.message)
    section = update.message.text
    
    for_compare = []
    res_compare = keyboard.find(section, main_db.load)

    if list(res_compare) != for_compare:
        keyboard.add_user_section(user_id = user.id, section = section)
        
    print("button_select::::", keyboard.user_path_section)

    msg, markup = keyboard.create_keyboard(section, user.id)
    user_last_section[user.id] = section
    context.bot.send_message(parse_mode = 'HTML', chat_id = user.id, text = msg, reply_markup = markup)

def return_to_section_before(update, context):
    user = User(update.message)

    keyboard.user_path_section[user.id].pop()
    section = keyboard.user_path_section[user.id][-1]

    msg, markup = keyboard.create_keyboard(section, user.id)
    context.bot.send_message(parse_mode = 'HTML', chat_id = user.id,text = msg, reply_markup = markup)

def main():
    updater = Updater(token = TOKEN, use_context = True)
    dp = updater.dispatcher

    start_handler = CommandHandler('start', send_start)
    
    back_to_main_menu = MessageHandler(Filters.regex('На главную'), return_to_main_menu)
    section_back = MessageHandler(Filters.regex('Назад'), return_to_section_before)
    button_select = MessageHandler(Filters.text, button_selection)

    # Обработчик разговора команды /admin
    conv_handler = ConversationHandler(
        entry_points = [ CommandHandler("admin", start_admin)],

         states={
            SELECTING_ACTION: [CallbackQueryHandler(ask_for_input)],
            TYPING: [MessageHandler(Filters.text, save_input)],
            END: [CallbackQueryHandler(cancel)]
        },

        fallbacks = [CommandHandler("admin", start_admin)],
    )

    dp.add_handler(start_handler)
    
    # обработчик разговора
    dp.add_handler(conv_handler)
    
    dp.add_handler(back_to_main_menu)
    dp.add_handler(section_back)
    dp.add_handler(button_select)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
