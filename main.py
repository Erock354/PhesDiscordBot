import random
from datetime import datetime
import os.path
import os
from code import discord_token
import discord
from discord.ext import commands
from waifu_service import get_url
from images_service import get_image, get_reaction
from data_handler import dir_init

# Permessi
intents = discord.Intents.all()
intents.message_content = True

# Setting del bot
client = commands.Bot(command_prefix='$', intents=intents, description='Fes gaming', help_command=None)


# Questo evento viene eseguito appena viene avviato il Bot
@client.event
async def on_ready():
    # Tipo di attività (in questo caso listening)
    activity_type = discord.ActivityType.playing

    # Nome dell'attività (posso metterci dentro quello che voglio)
    activity_name = 'with your balls'

    # Setting della presence (Attività)
    await client.change_presence(activity=discord.Activity(type=activity_type, name=activity_name))

    # Inserimento dei Cog (gruppi di comandi, eventi...)
    await client.add_cog(CommandErrorHandler(client))
    await client.add_cog(Test(client))
    await client.add_cog(Anime(client))
    await client.add_cog(Image(client))

    # Appena viene avviato manda un messaggio nel terminale
    print('I am ready for the use')
    print(' ')


# Cog test
# I Cog possiamo vederli come degli insiemi di comandi
# Questo insieme contiene solo un comando hello che risponde con hello o un differente messaggio se eseguito due volte
# di fila dalla stessa persona
class Test(commands.Cog):

    # __inti__ è letteralmente il costruttore del Cog.
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # Comando hello. Per creare dei comandi all'interno dei Cog devi usare il decoratore @commands.command()
    # Esistono altri modi ma io uso questo perché è comodo

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}~')
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar.')
        self._last_member = member


# Anime Cog (gruppo di comandi anime)
# Ogni comandi utilizza il metodo get_url() fornito dal waifu_service.py (guarda gli import)
# Ogni specifico comando passa diversi argomenti.
# In questo Cog ho inserito anche degli error handler per la gestione di eventuali errori.
class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def waifu(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        url = get_url('sfw', 'waifu')
        embed = discord.Embed(title='Waifu', description=f'Image gerenerated by {member.mention}', color=0xD8BFD8)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    # Questo è l'error handler del comando waifu().
    # Si costruiscono @nome_del_comando.error
    # Ogni volta che nel comando waifu avviene un errore questa funzione viene invocata
    # Nel mio caso, qualsiasi errore avvenga la risposta è sempre la stessa.
    @waifu.error
    async def waifu_error(self, ctx, error):
        print(error)
        await ctx.send('Something went wrong')

    @commands.command()
    async def neko(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        url = get_url('sfw', 'neko')
        embed = discord.Embed(title='Neko', description=f'Image gerenerated by {member.mention}', color=0xD8BFD8)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @neko.error
    async def neko_error(self, ctx, error):
        print(error)
        await ctx.send('Something went wrong')

    @commands.command()
    async def shinobu(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        url = get_url('sfw', 'shinobu')
        embed = discord.Embed(title='Shinobu', description=f'Image gerenerated by {member.mention}', color=0xD8BFD8)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @shinobu.error
    async def shinobu_error(self, ctx, error):
        print(error)
        await ctx.send('Something went wrong')

    @commands.command()
    async def megumin(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        url = get_url('sfw', 'megumin')
        embed = discord.Embed(title='Megumin', description=f'Image gerenerated by {member.mention}', color=0xD8BFD8)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @megumin.error
    async def megumin_error(self, ctx, error):
        print(error)
        await ctx.send('Something went wrong')

    @commands.command()
    async def bully(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        url = get_url('sfw', 'bully')
        embed = discord.Embed(title='Bully', description=f'Image gerenerated by {member.mention}', color=0xD8BFD8)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @bully.error
    async def bully_error(self, ctx, error):
        print(error)
        await ctx.send('Something went wrong')

    @commands.command()
    async def cuddle(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        url = get_url('sfw', 'cuddle')
        embed = discord.Embed(title='Cuddle', description=f'Image gerenerated by {member.mention}', color=0xD8BFD8)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @cuddle.error
    async def cuddle_error(self, ctx, error):
        print(error)
        await ctx.send('Something went wrong')


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply(f"' {ctx.message.content[1:]} ' doesn't exist.")


# Image Cog (gruppo di comandi Image)
# In questo gruppo ci sono tutti i comandi che manipolano le immagini fornite in input oppure vengono prese le propic
# degli user che invocano questi comandi.
class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def image(self, ctx, *args, member: discord.Member = None, avatar_path=None):

        if not os.path.exists(f'assets/guilds/{ctx.message.guild.id}/'):
            dir_init(ctx.message.guild.id)

        # Controlla se sono state messe due immagini ed è stato taggato qualcuno
        if len(ctx.message.attachments) >= 2 and ctx.message.mentions:
            await ctx.reply("You have to either attach a max of two images or an image with the mention of a user.")
            return

        # Contralla se le menzioni sono state fatte a dei ruoli. In caso invia un messaggio di errore.
        if ctx.message.role_mentions:
            await ctx.reply("You must mention an user.")
            return

        # Creazione della data ora
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

        # Controlla se esiste del testo nel comando. Se c'è la variabile 'text' verrà creata
        text: str = ''
        if args:
            for i in args:
                if not i[0] == '<':
                    text = text + i + " "
            text = text[:-1]
            f = open(f"assets/guilds/{ctx.message.guild.id}/texts.txt", "a")
            f.write(text + '\n')
            f.close()

        # Controlla se sono state menzionate delle persone nel comando
        if ctx.message.mentions:  # Sono state menzionate persone
            member = ctx.message.mentions[0]  # 'member' è la persona menzionata
        else:  # Non sono state menzionate persone
            member = member or ctx.author  # 'member' è la persona che ha invocato il comando

        # Controlla se ci sono file allegati al comando.
        if not ctx.message.attachments:  # Non ci sono file allegati

            # Salva la propic
            avatar_path = f'assets/pfps/{member.id}_pfp.png'
            await member.display_avatar.save(avatar_path)

            image_path = get_image(member_id=member.id, guild_id=ctx.message.guild.id, text=text)
            # L'immagine di sfondo sarà un caracal

        elif len(ctx.message.attachments) == 1:  # Ci sono file allegati

            avatar_path = f'assets/pfps/{member.id}_pfp.png'
            await member.display_avatar.save(avatar_path)

            extension = ctx.message.attachments[0].content_type[6:]  # Viene presa l'estensione del file come stringa

            # Controlla se l'esensione è valida. Estensioni valide: png, jpg, jpeg.
            # Se non è valida viene mandata una risposta la comando con il seguente messaggio. (comando interrotto)
            if extension != 'png' and extension != 'jpg' and extension != 'jpeg':
                await ctx.reply('Attached file not valid. The file must have one of those extension:'
                                ' **png**, **jpg** or **jpeg**.')
                return

            # Il file allegato viene salvato nel database
            attachment_path = f'assets/guilds/{ctx.message.guild.id}/attachments/{member.id}_{dt_string}_attachment.{extension} '
            await ctx.message.attachments[0].save(attachment_path)

            # Viene eseguito il metodo get_image() fornito da images_service.py
            image_path = get_image(member_id=member.id,
                                   guild_id=ctx.message.guild.id,
                                   attachment1_path=attachment_path,
                                   text=text)

        else:  # In questo caso ci sono più allegati. Nel caso noi prendiamo solo i primi due.

            extension1 = ctx.message.attachments[0].content_type[6:]  # Viene presa l'estensione del file come stringa
            extension2 = ctx.message.attachments[1].content_type[6:]

            # Controlla se l'esensione è valida. Estensioni valide: png, jpg, jpeg.
            # Se non è valida viene mandata una risposta la comando con il seguente messaggio. (comando interrotto)
            if extension1 != 'png' and extension1 != 'jpg' and extension1 != 'jpeg':
                await ctx.reply('Attached file n.1 not valid. The file must have one of those extension:'
                                ' **png**, **jpg** or **jpeg**.')
                return

            if extension2 != 'png' and extension2 != 'jpg' and extension2 != 'jpeg':
                await ctx.reply('Attached file n.2 not valid. The file must have one of those extension:'
                                ' **png**, **jpg** or **jpeg**.')
                return

            # Il file allegato viene salvato nel database
            attachment1_path = f'assets/guilds/{ctx.message.guild.id}/attachments/{member.id}_{dt_string}_attachment1.{extension1}'
            await ctx.message.attachments[0].save(attachment1_path)
            attachment2_path = f'assets/guilds/{ctx.message.guild.id}/attachments/{member.id}_{dt_string}_attachment2.{extension2}'
            await ctx.message.attachments[1].save(attachment2_path)

            # Viene eseguito il metodo get_image() fornito da images_service.py
            image_path = get_image(member_id=member.id,
                                   guild_id=ctx.message.guild.id,
                                   attachment1_path=attachment1_path,
                                   attachment2_path=attachment2_path,
                                   text=text)

        # 'image_path' rappresenta il percorso dell'immagine modificata all'interno del database

        # L'immagine viene allegata ad un Embed che poi verrà inviato in chat.
        # Immagine
        file = discord.File(image_path, filename="image.png")
        # Creazione dell'embed
        embed = discord.Embed(title='Image', description=f'Image gerenerated by {ctx.author.mention}',
                              color=0xD8BFD8)
        # Inserimento dell'immagine nell'embed
        embed.set_image(url="attachment://image.png")
        # Inserimento della data in fondo all'embed
        embed.set_footer(text=now.strftime("%m/%d/%Y %H:%M:%S"))

        # Invio dell'embed
        await ctx.send(file=file, embed=embed)
        # Cancellazione del comando inviato
        await ctx.message.delete()
        # Cancellazione dell'avatar
        if avatar_path is not None:
            os.remove(avatar_path)

    # Funzionamento molto simile al comando image()
    @commands.command()
    async def reaction(self, ctx, *, member: discord.Member = None, avatar_path=None):

        if not os.path.exists(f'assets/guilds/{ctx.message.guild.id}/'):
            dir_init(ctx.message.guild.id)

        # Controlla se sono state mandate file e se è stato menzionato qualcuno
        # Se tutte e due le azioni sono state eseguite il invia un messaggio di errore
        if ctx.message.mentions and ctx.message.attachments:
            await ctx.reply("You have to either attach an image or mention a user.")
            return

        # Contralla se le menzioni sono state fatte a dei ruoli. In caso invia un messaggio di errore.
        if ctx.message.role_mentions:
            await ctx.reply("You must mention an user.")
            return

        # Creazione della data ora
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

        # Esegue tutti i vari controlli elencati nel comando image()
        if ctx.message.mentions:
            member = ctx.message.mentions[0]
        else:
            member = member or ctx.author

        if not ctx.message.attachments:
            avatar_path = f'assets/pfps/{member.id}_pfp.png'
            await member.display_avatar.save(avatar_path)
            # Il metodo invocato qui è il get_reaction() fornito dal images_service.py
            image_path = get_reaction(member_id=member.id, guild_id=ctx.message.guild.id)

        else:
            # Controllo dell'estensione
            extension = ctx.message.attachments[0].content_type[6:]
            if extension != 'png' and extension != 'jpg' and extension != 'jpeg':
                await ctx.reply('Attached file not valid. The file must have one of those extension:'
                                ' **png**, **jpg** or **jpeg**.')
                return
            attachment_path = f'assets/guilds/{ctx.message.guild.id}/attachments/{member.id}_{dt_string}_attachment.{extension}'
            await ctx.message.attachments[0].save(attachment_path)
            # Il metodo invocato qui è il get_reaction() fornito dal images_service.py
            image_path = get_reaction(member_id=member.id, guild_id=ctx.message.guild.id,
                                      attachment_path=attachment_path)

        # Creazione e invio dell'embed
        file = discord.File(image_path, filename="image.png")
        embed = discord.Embed(title='Reaction', description=f'Reaction gerenerated by {ctx.author.mention}',
                              color=0xD8BFD8)
        embed.set_image(url="attachment://image.png")
        embed.set_footer(text=now.strftime("%m/%d/%Y %H:%M:%S"))

        await ctx.send(file=file, embed=embed)
        await ctx.message.delete()
        if avatar_path is not None:
            os.remove(avatar_path)

    @commands.command()
    async def avatar(self, ctx, *args, member: discord.Member = None):

        now = datetime.now()

        if ctx.message.mentions:
            member = ctx.message.mentions[0]
        else:
            member = member or ctx.author

        url = member.display_avatar.url
        embed = discord.Embed(title='Avatar', description=f'This is {member.mention} avatar',
                              color=0xD8BFD8)
        embed.set_image(url=url)
        embed.set_footer(text=now.strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)

    @commands.command()
    async def random(self, ctx, *, member: discord.Member = None):

        if not os.path.exists(f'assets/guilds/{ctx.message.guild.id}/'):
            dir_init(ctx.message.guild.id)

        try:
            attachment1_path = f"assets/guilds/{ctx.message.guild.id}/attachments/" + \
                               random.choice(os.listdir(f"assets/guilds/{ctx.message.guild.id}/attachments"))
            attachment2_path = f"assets/guilds/{ctx.message.guild.id}/attachments/" + \
                               random.choice(os.listdir(f"assets/guilds/{ctx.message.guild.id}/attachments"))
        except IndexError:
            await ctx.reply("The ***attachments*** directory of this server is empty.\n"
                            "You can fill the directory by using commands like: *image*, *reaction*... with "
                            "allegation. \n"
                            "The more images there are in the folder, the more possible random images will be "
                            "generated.")
            return

        member = member or ctx.author
        now = datetime.now()

        rand = random.randrange(0, 2)
        if rand == 0:
            lines = open(f"assets/guilds/{ctx.message.guild.id}/texts.txt").read().splitlines()
            text = random.choice(lines)
        else:
            text = ''

        image_path = get_image(member_id=member.id,
                               guild_id=ctx.message.guild.id,
                               attachment1_path=attachment1_path,
                               attachment2_path=attachment2_path,
                               text=text)

        file = discord.File(image_path, filename="image.png")
        embed = discord.Embed(title='Random', description=f'Random image generated by {ctx.author.mention}',
                              color=0xD8BFD8)

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text=now.strftime("%m/%d/%Y %H:%M:%S"))

        await ctx.send(file=file, embed=embed)

    @random.error
    async def random_error(self, ctx, error):
        print(error)
        await ctx.send('Something went wrong')

    @image.error
    async def image_error(self, ctx, error):
        print(error)
        await ctx.send('Something went wrong')

    @reaction.error
    async def reaction_error(self, ctx, error):
        print(error)
        await ctx.send('Something went wrong')


client.run(discord_token)
