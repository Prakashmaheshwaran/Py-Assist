from flask import Flask, request, jsonify, send_file
from addons.check_work import get_specs, generate_video
from addons.fetchpost import get_published_and_scheduled_posts
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

@app.route('/edit-video', methods=['GET'])
def edit_video():
    output_path = generate_video()
    return send_file(output_path, as_attachment=True, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(debug=True)
