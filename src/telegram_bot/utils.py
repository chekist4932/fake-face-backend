import ngrok

from src.config import NGROK_API_KEY

client = ngrok.Client(NGROK_API_KEY)
urls = []


def session():
    # generation card
    # get public url ngrok
    for tunnel in client.tunnels.list():
        urls.append(tunnel.public_url)

    public_url = urls[0]

    return public_url
