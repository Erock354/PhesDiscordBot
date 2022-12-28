from PIL import Image, ImageDraw
import PIL
from datetime import datetime
import random

reaction_path = f'assets/template/reaction.png'


# Metodo che permette di creare un immagine con sfondo a scelta, se non viene inserito nessun allegato sarà un caracal.
def get_image(member_id, guild_id, attachment1_path=None, attachment2_path=None):

    # Percorso dell'immagine da posizionare in basso a sx.
    til_path = f"assets/pfps/{member_id}_pfp.png"

    # Controlla se è stato passato il parametro attachment_path.
    # In caso non fosse stato passato lo sfondo sarà un caracal.
    # 'img_path' rappresenta il percorso dell'immagine di sfondo
    if attachment1_path is not None:
        img_path = attachment1_path

        if attachment2_path is not None:
            til_path = attachment2_path
    else:
        img_path = f"assets/caracal_images/caracal_{random.randrange(0, 100)}.png"

    # Viene creata un immagine e viene ridimensionata a 512x512
    img = PIL.Image.open(img_path)
    img = img.resize((512, 512))

    # Creazione data ora
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

    # Viene creata l'immagine che poi andrà in basso a sinistra, anche essa verrà ridimensionata
    til = Image.open(til_path)
    til = til.resize((128, 128))

    # Questo metodo inserisce un immagine in un altra (til dentro img) alle coordinate relative
    # Le coordinate rappresentano l'angolo in alto a sx dell'immagine inserita.
    img.paste(til, (12, 372))

    draw = ImageDraw.Draw(img)
    width = 10

    draw.line((130, 382) + (206, 306), width=width, fill="red")
    draw.line((176, 306) + (210, 306), width=width, fill="red")
    draw.line((206, 336) + (206, 302), width=width, fill="red")

    # 'image_path' rappresenta il percorso dell'immagine editata.
    image_path = f'assets/guilds/{guild_id}/generated_images/{dt_string}_{member_id}.png'
    # Salvataggio dell'immagine
    img.save(image_path)

    return image_path


# Metodo molto simile al get_image() ma qui viene presa l'immagine allegata, oppure la propic di chi ha invocato il
# comando o di un utente menzionato. Le immagini verranno inserite in un template.
def get_reaction(member_id, guild_id, attachment_path=None):
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
    image_path = f'assets/guilds/{guild_id}/generated_images/{dt_string}_{member_id}.png'
    img.save(image_path)
    return image_path
