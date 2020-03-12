import datetime
import logging
import os

import telebot
from telebot import apihelper
from telebot import types


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PROXY_IP = os.getenv("TELEGRAM_PROXY_IP")
PROXY_PORT = os.getenv("TELEGRAM_PROXY_PORT")

PAGINATION = os.getenv("PAGINATION")

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

if os.getenv("USE_PROXY") == "true":
    apihelper.proxy = {'https':f'socks5h://{PROXY_IP}:{PROXY_PORT}'}

bot = telebot.TeleBot(BOT_TOKEN)

electronics_list = [
    'Apple', 'Samsung', 'Nokia', 'Sony', 'Canon', 'Panasonic', 
    'Bose', 'Microsoft', 'LG', 'Intel', 'Nvidia', 'Dell', 'IBM', 
    'Acer', 'Asus', 'Lenovo', 'Xiaomi', 'Huawei']


def paging_items(lst, items_count):
    """ Подготовка списка и разбиение его на страницы """
    items = lst[:]
    items.sort()
    items = [f"{i + 1}. {items[i]}" for i in range(0, len(items))]
    return [items[i:i + items_count] for i in range(0, len(items), items_count)]


def hello_message():
    """ Приветственное сообщение, зависимое от времени суток """
    current_hour = datetime.datetime.now().hour
    if 0 <= current_hour < 6:
        message = "Доброй ночи"
    if 6 <= current_hour < 12:
        message = "Доброе утро"
    if 12 <= current_hour < 18:
        message = "Добрый день"
    if 18 <= current_hour <= 23:
        message = "Добрый вечер"
    return message


def start_keyboard():
    """ Стартовая клавиатура """
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text="Список производителей электроники:",
            callback_data="get_list"))
    return keyboard


def items_keyboard(call_data):
    """ Клавитура со списком производителей """
    keyboard = types.InlineKeyboardMarkup()
    items = paging_items(electronics_list, int(PAGINATION))
    pages = len(items)
    if call_data == "new":
        page = 0
    if call_data.startswith("next"):
        page = int(call_data.split(",")[1])
        page += 1
    if call_data.startswith("prev"):
        page = int(call_data.split(",")[1])
        page -= 1
    for item in items[page]:
        keyboard.add(
            types.InlineKeyboardButton(
                text=item,
                callback_data=item))
    if page == 0:
        keyboard.add(
            types.InlineKeyboardButton(
                text="Назад",
                callback_data="back"),
            types.InlineKeyboardButton(
                text=">>",
                callback_data=f"next,{page}"))
    elif page < pages - 1:
        keyboard.add(
            types.InlineKeyboardButton(
                text="Назад",
                callback_data="back"),
            types.InlineKeyboardButton(
                text="<<",
                callback_data=f"prev,{page}"),
            types.InlineKeyboardButton(
                text=">>",
                callback_data=f"next,{page}"))
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text="Назад",
                callback_data="back"),
            types.InlineKeyboardButton(
                text="<<",
                callback_data=f"prev,{page}"))
    return keyboard


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=hello_message(),
        reply_markup=start_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if (call.data == 'get_list'):
            bot.edit_message_text(chat_id=call.message.chat.id,
                     message_id=call.message.message_id,
                     text="Список производителей электроники:",
                     reply_markup=items_keyboard("new"),
                     parse_mode="HTML")

    if (call.data.startswith('next')):
            bot.edit_message_text(chat_id=call.message.chat.id,
                     message_id=call.message.message_id,
                     text="Список производителей электроники:",
                     reply_markup=items_keyboard(call.data),
                     parse_mode="HTML")

    if (call.data.startswith('prev')):
            bot.edit_message_text(chat_id=call.message.chat.id,
                     message_id=call.message.message_id,
                     text="Список производителей электроники:",
                     reply_markup=items_keyboard(call.data),
                     parse_mode="HTML")

    if (call.data == 'back'):
            bot.edit_message_text(chat_id=call.message.chat.id,
                     message_id=call.message.message_id,
                     text=hello_message(),
                     reply_markup=start_keyboard(),
                     parse_mode="HTML")


if __name__ == '__main__':
    bot.polling()

