import requests


def get_url(type: str, category: str):
    r = requests.get(f'https://api.waifu.pics/{type}/{category}')
    json = r.json()
    return json['url']
