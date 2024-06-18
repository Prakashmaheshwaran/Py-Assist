from flask import Flask, request, jsonify, send_file
from addons.specs import get_specs
from addons.fetchpost import get_published_and_scheduled_posts
from addons.post_update import update_post_media_and_seo
from addons.image_upload import fetch_and_upload_image
import threading
import time
import moviepy.editor as mpy
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "This is an API page"

@app.route('/specs', methods=['GET'])
def specs_route():
    return get_specs()

@app.route('/get-posts', methods=['POST'])
def get_posts_endpoint():
    data = request.json
    account_suffix = data.get('account_suffix')
    wp_url = data.get('wp_url')
    wp_username = data.get('wp_username')
    wp_password = data.get('wp_password')

    if not all([account_suffix, wp_url, wp_username, wp_password]):
        return jsonify({"error": "All credentials are required"}), 400

    try:
        posts = get_published_and_scheduled_posts(account_suffix, wp_url, wp_username, wp_password)
        return jsonify({"posts": posts})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/fetch-and-upload-image', methods=['POST'])
def fetch_and_upload_image_endpoint():
    data = request.json
    keyword = data.get('keyword')
    account_suffix = data.get('account_suffix')
    wp_url = data.get('wp_url')
    wp_username = data.get('wp_username')
    wp_password = data.get('wp_password')

    if not all([keyword, account_suffix, wp_url, wp_username, wp_password]):
        return jsonify({"error": "All required fields (keyword, account_suffix, wp_url, wp_username, wp_password) must be provided"}), 400

    try:
        # Fetch and upload the image to WordPress
        image_id, uploaded_image_url = fetch_and_upload_image(keyword, account_suffix, wp_url, wp_username, wp_password)
        if image_id is None:
            return jsonify({"error": "Failed to upload image"}), 500
        return jsonify({"wp_image_id": image_id, "wp_image_url": uploaded_image_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/update-post', methods=['POST'])
def update_post_endpoint():
    data = request.json
    account_suffix = data.get('account_suffix')
    post_id = data.get('post_id')
    focuskw = data.get('focuskw')
    seo_title = data.get('seo_title')
    meta_desc = data.get('meta_desc')

    if not all([account_suffix, post_id, focuskw, seo_title, meta_desc]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        updated_post = update_post_media_and_seo(account_suffix, post_id, focuskw, seo_title, meta_desc)
        return jsonify(updated_post)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

@app.route('/edit-video', methods=['GET'])
def edit_video():
    video = mpy.VideoClip(make_frame, duration=5).set_duration(5)
    video = video.set_fps(24)

    output_path = os.getenv('VIDEO_OUTPUT_PATH', 'hello_video.mp4')
    video.write_videofile(output_path, codec='libx264')

    return send_file(output_path, as_attachment=True, mimetype='video/mp4')


if __name__ == '__main__':
    app.run(debug=True)
