import platform
import psutil,os
from flask import jsonify
import moviepy.editor as mpy
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import ImageClip, ColorClip, TextClip

def get_specs():
    cpu_freq = psutil.cpu_freq()
    specs = {
        "CPU": platform.processor(),
        "Memory": f"{psutil.virtual_memory().total / (1024.0 ** 3):.2f} GB",
        "Storage": f"{psutil.disk_usage('/').total / (1024.0 ** 3):.2f} GB",
        "CPU Frequency": f"{cpu_freq.current / 1000:.2f} GHz"
    }
    return jsonify(specs)

def make_frame(t):
    # Create a blank frame with white background
    frame = mpy.ColorClip(size=(400, 600), color=(255, 255, 255)).to_ImageClip().get_frame(t)
    # Create text clip
    text_clip = mpy.TextClip("Hello", fontsize=50, color='black')
    # Calculate text position
    text_width, text_height = text_clip.size
    x_pos = 400 - text_width - t * (400 / 5)  # Move from right to left over 5 seconds
    y_pos = 100  # Fixed y position
    # Composite text on frame
    final_frame = mpy.CompositeVideoClip([mpy.ImageClip(frame), text_clip.set_position((x_pos, y_pos))]).get_frame(t)
    return final_frame

def generate_video():
    video = mpy.VideoClip(make_frame, duration=5).set_duration(5)
    video = video.set_fps(24)

    output_path = os.getenv('VIDEO_OUTPUT_PATH', 'hello_video.mp4')
    video.write_videofile(output_path, codec='libx264')

    return output_path