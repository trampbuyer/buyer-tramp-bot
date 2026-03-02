import telebot
from telebot import types
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

orders = {}
order_counter = 1

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🛍 Сделать заказ")
    btn2 = types.KeyboardButton("📦 Проверить статус")
    btn3 = types.KeyboardButton("💬 Связаться с байером")
    markup.add(btn1, btn2)
    markup.add(btn3)
    bot.send_message(message.chat.id, "Добро пожаловать в buyer_Tramp 💙", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🛍 Сделать заказ")
def make_order(message):
    msg = bot.send_message(message.chat.id, "Введите ссылку на товар:")
    bot.register_next_step_handler(msg, get_link)

def get_link(message):
    global order_counter
    link = message.text
    msg = bot.send_message(message.chat.id, "Введите размер:")
    bot.register_next_step_handler(msg, get_size, link)

def get_size(message, link):
    size = message.text
    msg = bot.send_message(message.chat.id, "Введите цвет:")
    bot.register_next_step_handler(msg, get_color, link, size)

def get_color(message, link, size):
    global order_counter
    color = message.text

    orders[order_counter] = {
        "link": link,
        "size": size,
        "color": color,
        "status": "В работе"
    }

    bot.send_message(message.chat.id, f"Ваш заказ №{order_counter} принят ✅\nСтатус: В работе")
    order_counter += 1

@bot.message_handler(func=lambda message: message.text == "📦 Проверить статус")
def check_status(message):
    msg = bot.send_message(message.chat.id, "Введите номер заказа:")
    bot.register_next_step_handler(msg, send_status)

def send_status(message):
    try:
        number = int(message.text)
        if number in orders:
            status = orders[number]["status"]
            bot.send_message(message.chat.id, f"Статус заказа №{number}: {status}")
        else:
            bot.send_message(message.chat.id, "Заказ не найден")
    except:
        bot.send_message(message.chat.id, "Введите корректный номер заказа")

@bot.message_handler(func=lambda message: message.text == "💬 Связаться с байером")
def contact(message):
    bot.send_message(message.chat.id, "Напишите сюда: @buyer_Tramp")

bot.polling()
