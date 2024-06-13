from moviepy.editor import *
from moviepy.video.tools.drawing import color_gradient

def create_hello_video():
    width, height = 1080, 1920
    duration = 5  # seconds

    # Create a video clip with a white background
    bg_clip = ColorClip(size=(width, height), color=(255, 255, 255), duration=duration)

    # Create a text clip using moviepy's TextClip
    txt_clip = TextClip("Hello", fontsize=70, color='black', font="Arial-Bold")
    txt_clip = txt_clip.set_duration(duration)

    # Animate the text sliding in from the left
    txt_clip = txt_clip.set_position(lambda t: (width * (1 - t / duration), 'center'))

    # Composite the text clip on the background
    video = CompositeVideoClip([bg_clip, txt_clip])

    # Write the video file
    output_path = "output.mp4"
    video.write_videofile(output_path, fps=24)
    return output_path
