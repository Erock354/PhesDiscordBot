import os


def dir_init(guild_id):
    guild_path = os.path.join('assets/guilds/', f'{guild_id}')
    attachments_path = os.path.join(f'assets/guilds/{guild_id}', 'attachments')
    generate_images_path = os.path.join(f'assets/guilds/{guild_id}', 'generated_images')

    os.mkdir(guild_path)
    os.mkdir(attachments_path)
    os.mkdir(generate_images_path)

    f = open(f"assets/guilds/{guild_id}/texts.txt", "a")
    f.write('balls\n')
    f.close()
