from telegram import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup)
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

user_last_section = {}


SELECTING_ACTION, ADDING_SECTION, EDIT_SECTION, CURRENT_FEATURE, TYPING, FEATURES = range(6)

# Shortcut for ConversationHandler.END
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
        InlineKeyboardButton(text='Выход из панели', callback_data = str(ConversationHandler.END))
    ]]
    kkeyboard = InlineKeyboardMarkup(buttons)

    update.message.reply_text('У администратора есть возможность добавлять разделы и их контекст. '\
            'Вы будете видеть, в каком разделе находитесь в данный момент.')

    sections = []
    try:
        currentSection = user_last_section[user.id]
        section = keyboard.find(currentSection, main_db.load)
        sections = list(section)[0]
        # TODO: refresh keyboard
        keyboard.create_keyboard(currentSection)
    except KeyError:
        sections = main_db.get_dump()
        # TODO: refresh keyboard
        ReplyKeyboardMarkup(keyboard.main_menu())

    update.message.reply_text(text = sections, reply_markup = kkeyboard)

    # context.user_data[START_OVER] = False
    return SELECTING_ACTION
    

def create_section(update, context):
    user = User(update.message)
    new_section_name = context.user_data["text"]

    try:
        currentSection = user_last_section[user.id]
        section = keyboard.find(currentSection, main_db.load)
        list(section)[0][new_section_name] = { 'text_msg': '' }
    except KeyError:
        main_db.load[new_section_name] = { 'text_msg': '' }

    keyboard.load = main_db.load
    main_db.save_db(main_db.load)
    

def edit_section(update, context):
    user = User(update.message)
    currentSection = user_last_section[user.id]

    new_section_text = update.message.text

    if currentSection is None:
        # main_db.load[new_section_name]['text_msg'] = new_section_text
        return
    else:
        section = keyboard.find(currentSection, main_db.load)
        list(section)[0]['text_msg'] = new_section_text

    main_db.save_db(main_db.load)

    return ConversationHandler.END

def ask_for_input(update, context):
    """Prompt user to input data for selected feature."""
    text = 'Окей, пиши.'

    context.user_data["func"] = update.callback_query.data

    update.callback_query.answer()
    update.callback_query.edit_message_text(text = text)

    return TYPING


def save_input(update, context):
    """Save input for feature and return to feature selection."""
    
    context.user_data["text"] = update.message.text

    if context.user_data["func"] == str(ADDING_SECTION):
        create_section(update, context)
    else:
        pass

    return start_admin(update, context)

def cancel(update, context):
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup = ReplyKeyboardRemove())

    return ConversationHandler.END


"""Работа с пользователем"""
def send_start(update, context):
    user = User(update.message)

    if user.id in user_db.users:
        context.bot.send_photo(chat_id = user.id, photo = random.choice(photo))
        context.bot.send_message(chat_id = user.id, text = random.choice(msg).format(name = user.username), reply_markup = keyboard.main_menu())
        
        if user.is_admin:
            context.bot.send_message(parse_mode = 'HTML', chat_id = user.id, text = 'У вас есть <b><i>права</i></b> администратора, введите команду /admin, чтобы внести изменения.🎉')
            # print([*main_db.load])
            # context.bot.send_message(chat_id = user.id, text = json.dumps([*main_db.load], ensure_ascii = False))
    else: 
        context.bot.send_photo(chat_id = user.id, photo = random.choice(photo))
        context.bot.send_message(chat_id = user.id, text = random.choice(msg1).format(name = user.username), reply_markup = keyboard.main_menu())
        user_db.save_user(user.id)
    

def return_to_main_menu(update, context):  
    user = User(update.message) 
    keyboard.main_menu()
    context.bot.send_message(chat_id = user.id, text = 'Хорошо, сделано.', reply_markup = keyboard.main_menu())


def button_selection(update, context):
    user = User(update.message)
    section = update.message.text
    
    msg, markup = keyboard.create_keyboard(section)

    user_last_section[user.id] = section

    context.bot.send_message(chat_id = user.id,text = msg, reply_markup = markup)

def main():
    updater = Updater(token = TOKEN, use_context = True)
    dp = updater.dispatcher

    start_handler = CommandHandler('start', send_start)
    
    msg_handler1 = MessageHandler(Filters.regex('На главную'), return_to_main_menu)
    msg_handler2 = MessageHandler(Filters.text, button_selection)

    # selection_handlers = [
    #     CallbackQueryHandler(create_section, pattern='^' + str(ADDING_SECTION) + '$'),
    #     CallbackQueryHandler(callback_handler),
    #     CallbackQueryHandler(edit_section, pattern='^' + str(EDIT_SECTION) + '$'),
    #     CallbackQueryHandler(cancel, pattern='^' + str(ConversationHandler.END) + '$'),
    # ]

    # Set up top level ConversationHandler (selecting action)
    conv_handler = ConversationHandler(
        entry_points = [ CommandHandler("admin", start_admin)],

        # states = { SELECTING_ACTION: selection_handlers,},
         states={
            SELECTING_ACTION: [CallbackQueryHandler(ask_for_input,
                                                     pattern='^(?!' + str(END) + ').*$')],
            TYPING: [MessageHandler(Filters.text, save_input)],
        },

        fallbacks = [ ],
    )

    dp.add_handler(start_handler)
    
    # обработчик разговора
    dp.add_handler(conv_handler)
    
    dp.add_handler(msg_handler1)
    dp.add_handler(msg_handler2)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
    # a = main_db.load
    # d = keyboard.find("Глава2", a)
    # list(d)[0]["Параграф2.1"]["text_msg"] = "PASHOL NAXYI"
    # print(a)
    # main_db.save_db()




    # in_memory_db = {}

    # uid = 128376
    # key = "шлава1"

    # in_memory_db[uid] = key
