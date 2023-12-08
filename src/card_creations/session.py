import json
from hashlib import sha256

import ngrok


from src.utils import gen_fake_card
from src.config import NGROK_API_KEY


client = ngrok.Client(NGROK_API_KEY)
urls = []


def session(card_data: dict):

    # generation card
    gen_fake_card(card_data)
    print('card generated')
    # get public url ngrok
    for tunnel in client.tunnels.list():
        urls.append(tunnel.public_url)

    public_url = urls[0] + '/pass'

    return public_url
