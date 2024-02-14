import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent

API_TOKEN = os.environ.get('TG_API_TOKEN')
NGROK_API_KEY = os.environ.get('NGROK_API_KEY')

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')

ALGORITHM = os.environ.get("ALGORITHM")

PRIVATE_KEY_PATH = BASE_DIR / "certs" / "private.pem"
PUBLIC_KEY_PATH = BASE_DIR / "certs" / "public.pem"

PATH_TO_PHOTOS = BASE_DIR / "static" / "photos"
PATH_TO_CARD_SOURCE = BASE_DIR / "static" / "card_source"
PATH_TO_CARDS = BASE_DIR / "static" / "cards"


# PATH_TO_PHOTOS = os.environ.get('PATH_TO_PHOTOS')
# PATH_TO_CARD_SOURCE = os.environ.get('PATH_TO_CARD_SOURCE')
# PATH_TO_CARDS = os.environ.get('PATH_TO_CARDS')
