from datetime import datetime
import os.path
from code import discord_token
import discord
from discord.ext import commands
from waifu_service import get_url
from images_service import get_image, get_reaction

intents = discord.Intents.all()
intents.message_content = True

client = commands.Bot(command_prefix='$', intents=intents, description='Fes gaming', help_command=None)


@client.event
async def on_ready():
    activity_type = discord.ActivityType.listening
    activity_name = 'Women Punch'
    await client.change_presence(activity=discord.Activity(type=activity_type, name=activity_name))
    await client.add_cog(CommandErrorHandler(client))
    await client.add_cog(Test(client))
    await client.add_cog(Anime(client))
    await client.add_cog(Image(client))
    print('I am ready for the use')
    print(' ')


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}~')
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar.')
        self._last_member = member


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
            await ctx.reply(f"**{ctx.message.content[1:]}** doesn't exist.")


class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def image(self, ctx, *args, member: discord.Member = None):
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

        if ctx.message.mentions:
            member = ctx.message.mentions[0]
        else:
            member = member or ctx.author

        if not os.path.exists(f'assets/pfps/{member.id}_pfp.png'):
            avatar_path = f'assets/pfps/{member.id}_pfp.png'
            await member.display_avatar.save(avatar_path)

        if not ctx.message.attachments:
            image_path = get_image(member_id=member.id)

        else:
            extension = ctx.message.attachments[0].content_type[6:]
            if extension != 'png' and extension != 'jpg' and extension != 'jpeg':
                await ctx.reply('Attached file not valid. The file must have one of those extension:'
                                ' **png**, **jpg** or **jpeg**.')
                return

            attachment_path = f'assets/attachments/{member.id}_{dt_string}_attachment.{extension}'
            await ctx.message.attachments[0].save(attachment_path)
            image_path = get_image(member_id=member.id, attachment_path=attachment_path)

        file = discord.File(image_path, filename="image.png")
        embed = discord.Embed(title='Reaction', description=f'Image gerenerated by {ctx.author.mention}',
                              color=0xD8BFD8)
        embed.set_image(url="attachment://image.png")
        embed.set_footer(text=now.strftime("%m/%d/%Y/ %H:%M:%S"))

        await ctx.send(file=file, embed=embed)
        await ctx.message.delete()

    @commands.command()
    async def reaction(self, ctx, *args, member: discord.Member = None):

        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

        if ctx.message.mentions:
            member = ctx.message.mentions[0]
        else:
            member = member or ctx.author

        if not os.path.exists(f'assets/pfps/{member.id}_pfp.png'):
            avatar_path = f'assets/pfps/{member.id}_pfp.png'
            await member.display_avatar.save(avatar_path)

        if not ctx.message.attachments:
            image_path = get_reaction(member_id=member.id)

        else:
            extension = ctx.message.attachments[0].content_type[6:]
            if extension != 'png' and extension != 'jpg' and extension != 'jpeg':
                await ctx.reply('Attached file not valid. The file must have one of those extension:'
                                ' **png**, **jpg** or **jpeg**.')
                return

            attachment_path = f'assets/attachments/{member.id}_{dt_string}_attachment.{extension}'
            await ctx.message.attachments[0].save(attachment_path)
            image_path = get_reaction(member_id=member.id, attachment_path=attachment_path)

        file = discord.File(image_path, filename="image.png")
        embed = discord.Embed(title='Reaction', description=f'Reaction gerenerated by {ctx.author.mention}',
                              color=0xD8BFD8)
        embed.set_image(url="attachment://image.png")
        embed.set_footer(text=now.strftime("%m/%d/%Y/ %H:%M:%S"))

        await ctx.send(file=file, embed=embed)
        await ctx.message.delete()


client.run(discord_token)
