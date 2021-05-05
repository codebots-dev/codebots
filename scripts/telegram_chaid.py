from codebots.utilities.tokens import get_telegram_chatid
from codebots.bots import TeleBot

js = get_telegram_chatid('1698218724:AAG44XBJh_GMGhfNLw0PV6ZzJfiL7tsBu-I')
print(js['result'][0]['message']['chat']['id'])
