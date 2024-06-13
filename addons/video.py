from moviepy.editor import *
import os

def create_hello_video():
    # Define the size of the video
    width, height = 1080, 1920  # Portrait mode resolution

    # Create a text clip
    txt_clip = TextClip("Hello", fontsize=70, color='black', font="Arial-Bold")

    # Position the text off-screen to the left initially and animate it sliding in
    txt_clip = txt_clip.set_position(lambda t: (int(width * (0.5 - t / 5.0)), height / 2 - txt_clip.h / 2)) \
                       .set_start(0).set_duration(5)

    # Create a white background clip
    bg_clip = ColorClip(size=(width, height), color=(255, 255, 255), duration=5)

    # Composite the text clip on the background
    video = CompositeVideoClip([bg_clip, txt_clip])

    # Write the video file
    output_path = "output.mp4"
    video.write_videofile(output_path, fps=24)

    return output_path
