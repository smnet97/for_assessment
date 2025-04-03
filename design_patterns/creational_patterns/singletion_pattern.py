"""
Singleton Pattern

Maqsad: Bir sinfdan faqat bitta obyejt yaratilishini ta’minlash.

Qachon ishlatiladi: Masalan, dasturda bitta konfiguratsiya fayli yoki logger bo’lishi kerak bo’lsa.
"""

class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

# Test qilamiz
obj1 = Singleton()
obj2 = Singleton()
print(obj1 is obj2)  # True - ikkalasi bir xil obyekt


# example

import requests
import logging
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv("main/.env")
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


# Telegramga xabar yuborish funksiyasi
def send_telegram_message(message):
    try:
        response = requests.post(TELEGRAM_API_URL, data={
            "chat_id": CHAT_ID,
            "text": message
        })
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Telegramga yuborishda xatolik: {e}")


# Logger sozlamalari
class TelegramLogHandler(logging.Handler):
    _instance = None

    def emit(self, record):
        log_entry = self.format(record)
        send_telegram_message(log_entry)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TelegramLogHandler, cls).__new__(cls)
        return cls._instance


# Logger yaratish
logger = logging.getLogger("TelegramLogger")
logger.setLevel(logging.INFO)

# Telegram log handler qo'shish
telegram_handler = TelegramLogHandler()
t = TelegramLogHandler()
print(telegram_handler is t)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
telegram_handler.setFormatter(formatter)
logger.addHandler(telegram_handler)

logger.info('test')