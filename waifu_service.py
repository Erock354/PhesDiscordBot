import random
import traceback

import requests
from code import danbooru_api_key
from pybooru import Danbooru


# Richiesta http
# Questo metodo 2 parametri
# 'type': NSFW oppure SFW
# 'category': In base al comando viene inserita una categoria. es: waifu, neko, shinobu...
def get_url(type: str, category: str):
    r = requests.get(f'https://api.waifu.pics/{type}/{category}')
    json = r.json()
    return json['url']


ext_img = ['png', 'jpg', 'jpeg', 'gif']
ext_vid = ['webm', 'mp4', 'zip']
client = Danbooru('danbooru', username='Erock', api_key=danbooru_api_key)


def get_post(args):
    if len(args) == 0:
        r = client.post_list(random=True)

    elif len(args) == 1:
        r = client.post_list(tags=args[0], random=True)
    else:
        tags = f'{args[0]} {args[1]}'
        r = client.post_list(tags=tags, limit=100)

    try:
        rand = random.randint(0, len(r) - 1)
        while True:
            if r[rand]['file_size'] < 7000000:
                break
            else:
                rand = random.randint(0, len(r) - 1)

        ext = r[rand]['file_ext']
        url = r[rand]['file_url']
        for x in ext_img:
            if x == ext:
                return [url, 'img']

        for x in ext_vid:
            if x == ext:
                return [url, ext]

        return 404

    except Exception:  # work on python 2.x
        traceback.print_exc()
        return 404
