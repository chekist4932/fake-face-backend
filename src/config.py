import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.environ.get('TG_API_TOKEN')
NGROK_API_KEY = os.environ.get('NGROK_API_KEY')

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')

SECRET_AUTH = os.environ.get("SECRET_AUTH")

PATH_TO_PHOTOS = os.environ.get('PATH_TO_PHOTOS')
PATH_TO_CARD_SOURCE = os.environ.get('PATH_TO_CARD_SOURCE')
PATH_TO_CARDS = os.environ.get('PATH_TO_CARDS')
