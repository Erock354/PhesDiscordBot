from moviepy.editor import *

fps_img = 2


def get_video(guild_id:str, image_path: str, audio_path: str):

    audio = AudioFileClip(audio_path)
    video_path = f'assets/guilds/{guild_id}/generated_stuff/video.mp4'

    print(audio.duration)

    if audio.duration > 30:
        audio.close()
        return 400

    if audio.duration < 1:
        audio.close()
        return 401

    clip = ImageClip(img=image_path, duration=audio.duration)
    clip.audio = audio
    clip.write_videofile(video_path, fps=fps_img)
    clip.close()

    return video_path
