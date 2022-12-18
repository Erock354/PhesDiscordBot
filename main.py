import discord
from discord.ext import commands
import requests


intents = discord.Intents.all()
intents.message_content = True

client = commands.Bot(command_prefix='$', intents=intents, description='Fes gaming')


@client.event
async def on_ready():
    activity_type = discord.ActivityType.listening
    activity_name = 'Haritsuke no misa'
    await client.change_presence(activity=discord.Activity(type=activity_type, name=activity_name))
    await client.add_cog(Test(client))
    await client.add_cog(Anime(client))
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
        """Says hello"""
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
        r = requests.get('https://api.waifu.pics/sfw/waifu')
        json = r.json()
        embed=discord.Embed(title='waifu', description=f'Image gerenerated by {member.mention}', color=0xD8BFD8)
        embed.set_image(url=json['url'])
        await ctx.send(embed=embed)


client.run('OTI3NTUyMDI1NTQwMDU1MDQw.GJehix.Ns8YuPPdSg78jtlHwQ4t8BJZ1CfWvGPUiKu_jk')
