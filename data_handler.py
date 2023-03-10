import os
import discord


def dir_init(guild_id):
    guild_path = os.path.join('assets/guilds/', f'{guild_id}')
    attachments_path = os.path.join(f'assets/guilds/{guild_id}', 'attachments')
    generated_images_path = os.path.join(f'assets/guilds/{guild_id}', 'generated_stuff')
    audio_path = os.path.join(f'assets/guilds/{guild_id}', 'audio')

    os.mkdir(guild_path)
    os.mkdir(attachments_path)
    os.mkdir(generated_images_path)
    os.mkdir(audio_path)

    f = open(f"assets/guilds/{guild_id}/texts.txt", "a")
    f.write('balls\n')
    f.close()


def log(command_name: str, member: discord.Member, guild_id: int, time: str):
    print(f'Command {command_name} invoked by {member.name}#{member.discriminator} from guild <{guild_id}> has '
          f'finished his execution at {time}.')
