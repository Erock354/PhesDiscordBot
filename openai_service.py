import openai
from PIL import Image
import PIL
from code import openai_api_key
from datetime import datetime
import random


def openai_api_init():
    openai.api_key = openai_api_key


def get_image_with_caracal(member_id):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    caracal_path = f"assets/caracal_images/caracal_{random.randrange(0,100)}.png"
    img = PIL.Image.open(caracal_path)
    til = Image.open(f"assets/pfps/{member_id}_pfp.png")
    til = til.resize((128, 128))
    img.paste(til, (12, 372))

    image_path = f'assets/generated_images/{dt_string}_{member_id}.png'
    img.save(image_path)
    return image_path


def get_image_with_attachment(member_id, attachment_path):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    img = PIL.Image.open(attachment_path)
    img = img.resize((512, 512))
    til = Image.open(f"assets/pfps/{member_id}_pfp.png")
    til = til.resize((128, 128))
    img.paste(til, (12, 372))
    image_path = f'assets/generated_images/{dt_string}_{member_id}.png'
    img.save(image_path)
    return image_path

