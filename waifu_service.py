import requests


# Richiesta http
# Questo metodo 2 parametri
# 'type': NSFW oppure SFW
# 'category': In base al comando viene inserita una categoria. es: waifu, neko, shinobu...
def get_url(type: str, category: str):
    r = requests.get(f'https://api.waifu.pics/{type}/{category}')
    json = r.json()
    return json['url']
