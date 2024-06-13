from flask import Flask, request, jsonify, send_file
from addons.specs import get_specs
from addons.wordpressblogimagehelper import fetch_and_upload_image
from addons.fetchpost import get_published_and_scheduled_posts
from addons.postupdate import update_post_media_and_seo
from addons.video import create_hello_video  # Import the create_hello_video function
import threading
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "This is an API page"

@app.route('/specs', methods=['GET'])
def specs_route():
    return get_specs()

@app.route('/fetch-and-upload-image', methods=['GET'])
def fetch_and_upload_image_endpoint():
    keyword = request.args.get('keyword')
    account_suffix = request.args.get('account_suffix')
    if not keyword or not account_suffix:
        return jsonify({"error": "Keyword or account suffix not provided"}), 400

    try:
        image_id, image_url = fetch_and_upload_image(keyword, account_suffix)
        if image_id is None or image_url is None:
            return jsonify({"error": "Failed to upload image to WordPress"}), 500
        return jsonify({"wp_image_id": image_id, "wp_image_url": image_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-posts', methods=['GET'])
def get_posts_endpoint():
    account_suffix = request.args.get('account_suffix')
    if not account_suffix:
        return jsonify({"error": "Account suffix not provided"}), 400

    try:
        posts = get_published_and_scheduled_posts(account_suffix)
        return jsonify({"posts": posts})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update-post', methods=['POST'])
def update_post_endpoint():
    data = request.json
    account_suffix = data.get('account_suffix')
    post_id = data.get('post_id')
    new_image_id = data.get('new_image_id')
    focuskw = data.get('focuskw')
    seo_title = data.get('seo_title')
    meta_desc = data.get('meta_desc')

    if not all([account_suffix, post_id, new_image_id, focuskw, seo_title, meta_desc]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        updated_post = update_post_media_and_seo(account_suffix, post_id, new_image_id, focuskw, seo_title, meta_desc)
        return jsonify(updated_post)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Function to log duration every second
def long_running_task():
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        print(f"Task has been running for {int(elapsed_time)} seconds")
        time.sleep(1)

@app.route('/run-long-task', methods=['GET'])
def run_long_task():
    thread = threading.Thread(target=long_running_task)
    thread.daemon = True
    thread.start()
    return jsonify({"status": "Task started, check logs for duration updates"}), 200

# Endpoint to create and serve the video
@app.route('/create-video', methods=['GET'])
def create_video_endpoint():
    try:
        video_path = create_hello_video()
        return send_file(video_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
