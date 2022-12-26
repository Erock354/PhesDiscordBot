from PIL import Image
import PIL
from datetime import datetime
import random

reaction_path = f'assets/template/reaction.png'


def get_image(member_id, attachment_path=None):
    if attachment_path is not None:
        img_path = attachment_path
    else:
        img_path = f"assets/caracal_images/caracal_{random.randrange(0, 100)}.png"
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    img = PIL.Image.open(img_path)
    til = Image.open(f"assets/pfps/{member_id}_pfp.png")
    til = til.resize((128, 128))
    img.paste(til, (12, 372))

    image_path = f'assets/generated_images/{dt_string}_{member_id}.png'
    img.save(image_path)
    return image_path


def get_reaction(member_id, attachment_path=None):
    if attachment_path is not None:
        til_path = attachment_path
    else:
        til_path = f"assets/pfps/{member_id}_pfp.png"
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    img = PIL.Image.open(reaction_path)
    til1 = Image.open(til_path)
    til2 = Image.open(til_path)

    til1 = til1.resize((210, 70))
    img.paste(til1, (135, 20))

    til2 = til2.resize((616, 350))
    img.paste(til2, (10, 110))
    image_path = f'assets/generated_images/{dt_string}_{member_id}.png'
    img.save(image_path)
    return image_path
