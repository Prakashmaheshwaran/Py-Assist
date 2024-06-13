from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_text_image(text, size, font_size, font_path="fonts/Arial.ttf"):
    """ Create an image with the given text """
    image = Image.new('RGB', size, color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    text_size = draw.textsize(text, font=font)
    text_position = ((size[0] - text_size[0]) // 2, (size[1] - text_size[1]) // 2)
    draw.text(text_position, text, font=font, fill=(0, 0, 0))
    return np.array(image)

def create_hello_video():
    width, height = 1080, 1920
    duration = 5  # seconds

    # Create a video clip with a white background
    bg_clip = ColorClip(size=(width, height), color=(255, 255, 255), duration=duration)

    # Create the text image
    text_image = create_text_image("Hello", (width, height), font_size=70)

    # Create an ImageClip with the text image
    text_clip = ImageClip(text_image, duration=duration)

    # Animate the text sliding in from the left
    text_clip = text_clip.set_position(lambda t: (width * (1 - t / duration), 'center'))

    # Composite the text clip on the background
    video = CompositeVideoClip([bg_clip, text_clip])

    # Write the video file
    output_path = "output.mp4"
    video.write_videofile(output_path, fps=24)
    return output_path
