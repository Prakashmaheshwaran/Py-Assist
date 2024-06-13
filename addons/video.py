import moviepy.config as mpy_config
import os

# Ensure the ImageMagick binary path is set correctly
mpy_config.change_settings({"IMAGEMAGICK_BINARY": os.getenv("IMAGEMAGICK_BINARY", "/usr/bin/convert")})

from moviepy.editor import *

def create_hello_video():
    width, height = 1080, 1920
    txt_clip = TextClip("Hello", fontsize=70, color='black', font="Arial-Bold")
    txt_clip = txt_clip.set_position(lambda t: (int(width * (0.5 - t / 5.0)), height / 2 - txt_clip.h / 2)) \
                       .set_start(0).set_duration(5)
    bg_clip = ColorClip(size=(width, height), color=(255, 255, 255), duration=5)
    video = CompositeVideoClip([bg_clip, txt_clip])
    output_path = "output.mp4"
    video.write_videofile(output_path, fps=24)
    return output_path
