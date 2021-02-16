# -*- coding: utf-8 -*-
#info bot created by negative
import sys
import telebot
import json
import os
import datetime
import settings
import random
import requests as req
from telebot import types
from settings import KEYBOARD
import flask
from flask_sslify import SSLify

WEBHOOK_URL_BASE = "https://{}:{}".format(settings.WEBHOOK_HOST, settings.WEBHOOK_PORT)

bot = telebot.TeleBot(settings.BOT_TOKEN, threaded=True)

# удаляем предыдущие вебхуки, если они были
bot.remove_webhook()

# ставим новый вебхук = Слышь, если кто мне напишет, стукни сюда — url
bot.set_webhook(url=WEBHOOK_URL_BASE + settings.WEBHOOK_PATH)

app = flask.Flask(__name__)
sslify = SSLify(app)

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row( KEYBOARD['ID_INFO'])
keyboard.row(KEYBOARD['DI_MY'], KEYBOARD['ID_HELP'])

@bot.message_handler(commands=['start'])
def welcome(m):
    cid = m.chat.id
    msg = 'Вітаю {} 😊, я бот що показує твій ID (ідентифікатор) в Телеграмі, версія бота {} р.'.format(m.chat.first_name + ' ' + (m.chat.last_name or ''), settings.VERSION)
    ret_msg = bot.send_message(cid, msg, disable_notification=True, reply_markup=keyboard)
    assert ret_msg.message_id

@bot.message_handler(content_types=["text"])
def main_menu(message):
    name = message.from_user.first_name + ' ' + (message.from_user.last_name or '')
    cid = message.chat.id
    text = message.text    
    usr = message.chat.username
    f = message.chat.first_name
    l = message.chat.last_name
    t = message.chat.type
    d = message.date
    fc = message.from_user.language_code
    fcid = message.from_user.id
    ffirst = message.from_user.first_name
    flast = message.from_user.last_name
    fusr = message.from_user.username
    
    if message.text == KEYBOARD['DI_MY']:
        dtn = datetime.datetime.now()
        botlogfile = open('bot_id_logs.txt', 'a', encoding='utf-8')
        print(dtn.strftime("[%d-%m-%Y %H:%M:%S]:"), "({}, @{}, id:{}) -> {}".format(name, usr, fcid, text), file=botlogfile)
        botlogfile.close()
        msg = '<b>{}</b> Ваш ID = {}'.format(name, fcid)
        bot.send_message(cid, msg, parse_mode='HTML', reply_markup=keyboard)

    elif message.text == KEYBOARD['ID_INFO']:
        dtn = datetime.datetime.now()
        botlogfile = open('bot_id_logs.txt', 'a', encoding='utf-8')
        print(dtn.strftime("[%d-%m-%Y %H:%M:%S]:"), "({}, @{}, id:{}) -> {}".format(name, usr, fcid, text), file=botlogfile)
        botlogfile.close()
        msg = '<b>Ваш ID</b>: {} \n<b>Ваше ім\'я користувача</b>: @{} \n<b>Ваше ім\'я</b>: {}\n<b>Ваше прізвище</b>: {}\n<b>Тип</b>: {}\n<b>Дані запиту</b>: {}\n<b>Ваш запит</b>: {}\n<b>Мова</b>: {}'.format(cid,usr,f,l,t,d,text,fc)
        bot.send_chat_action(cid, "typing")
        bot.reply_to(message, msg, parse_mode='HTML', reply_markup=keyboard)

    elif message.text == KEYBOARD['ID_FBACK']:
        dtn = datetime.datetime.now()
        botlogfile = open('bot_id_logs.txt', 'a', encoding='utf-8')
        print(dtn.strftime("[%d-%m-%Y %H:%M:%S]:"), "({}, @{}, id:{}) -> {}".format(name, usr, fcid, text), file=botlogfile)
        botlogfile.close()
        str = message.text
        txt = str.replace('/feedback', '')
        bot.send_message(cid, "Дякую. Повідомлення відправлено розробнику", parse_mode='HTML', reply_markup=keyboard)
        bot.send_message(settings.ADMINS_ID, "Повідомлення від користувача: {}\nID: {}\nІм'я: {}\nПрізвище: {}\nІм'я користувача: @{}".format(txt,fcid,ffirst,flast,fusr))

    elif message.text == KEYBOARD['ID_HELP']:
        dtn = datetime.datetime.now()
        botlogfile = open('bot_id_logs.txt', 'a', encoding='utf-8')
        print(dtn.strftime("[%d-%m-%Y %H:%M:%S]:"), "({}, @{}, id:{}) -> {}".format(name, usr, fcid, text), file=botlogfile)
        botlogfile.close()
        msg = 'Вітаю {}, версія бота {}\n\n' \
              'Якщо вам потрібен доступ до телефоного довідника скопіюйте повну інформацію про ID та відправте її в чат бот ТА ДНЗ &quot;ДТРЕК&quot;'.format(name, settings.VERSION)
        bot.send_message(cid, msg, disable_notification=True, parse_mode='HTML', reply_markup=keyboard)
        
    else:
        msg = 'Не намагайтесь писати ботові він не розуміє. Він показує вам тільки вашу інформацію.'
        bot.send_message(cid, msg, parse_mode='HTML')

@bot.message_handler(content_types=['sticker'])
def handler_sticker(m):
    dtn = datetime.datetime.now()
    botlogfile = open('bot_id_logs.txt', 'a', encoding='utf-8')
    print(dtn.strftime("[%d-%m-%Y %H:%M:%S]:"), "({}, @{}, id:{}) -> {}".format(m.chat.first_name + ' ' + (m.chat.last_name or ''), m.chat.username, m.from_user.id, m.content_type), file=botlogfile)
    botlogfile.close()
    bot.send_message(m.chat.id, "<b>Стікер ID</b>: " + m.sticker.file_id, parse_mode='HTML')

@bot.message_handler(commands=['log'])
def text(m):
    if m.chat.id == settings.ADMINS_ID:
        file = open('bot_id_logs.txt', 'rb')
        bot.send_document(m.chat.id, file)
    else:
        bot.send_message(m.chat.id, settings.NO_ADMIN)
        

# пустая главная страничка для проверки
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм 
@app.route(settings.WEBHOOK_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

# Start polling server
#bot.polling(interval=settings.POLLING_INTERVAL, timeout=settings.POLLING_TIMEOUT, none_stop=True)

# Start flask server
app.run(host=settings.WEBHOOK_LISTEN,
        port=settings.WEBHOOK_PORT,
        ssl_context=(settings.WEBHOOK_SSL_CERT, settings.WEBHOOK_SSL_PRIV),
        debug=settings.WEBHOOK_DEBUG)