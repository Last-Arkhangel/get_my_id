# -*- coding: utf-8 -*-
import os

# если выкладываем на heroku
WEBHOOK_HOST = ''

# телеграм может работать с портами 443, 80, 88 или 8443
WEBHOOK_PORT = '8443'

# In some VPS you may need to put here the IP addr
WEBHOOK_LISTEN = '192.168.1.1'  

# Path to the ssl certificate
WEBHOOK_SSL_CERT = 'server.crt'  

# Path to the ssl private key
WEBHOOK_SSL_PRIV = 'server.key'  

# Path that telegram sends updates
WEBHOOK_PATH = "/get_my_id/"

# Bot version
VERSION = '1.1.1 від 04.01.2021'

# Admin id: my
ADMINS_ID = 112233445

#not admin
NO_ADMIN = "Ви не адміністратор 👿!"

# Add Your Token
BOT_TOKEN = ''

# Interval to polling telegram servers 
POLLING_INTERVAL = 2

# Timeout to polling telegram servers
POLLING_TIMEOUT = 25

# Debug 'True sets False'
WEBHOOK_DEBUG = False

KEYBOARD = {
    'ID_INFO': '\U0001F9FE Повна інформація про ID',
    'DI_MY': '\U0001F194 Ваш ID',
    'ID_FBACK': '\U0001F51D Відправити',
    'ID_HELP': '\U0001F4AC Довідка',
}