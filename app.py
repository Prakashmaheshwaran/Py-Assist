from flask import Flask, request, jsonify, send_file
from addons.specs import get_specs
from addons.fetchpost import get_published_and_scheduled_posts
from addons.postupdate import update_post_media_and_seo
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

@app.route('/edit-video', methods=['GET'])
def edit_video():
    def make_frame(t):
        text = mpy.TextClip("Hello", fontsize=70, color='white')
        text = text.set_position((min(int(t*100), 500), 'center')).set_duration(5)
        return text.get_frame(t)

    video = mpy.VideoClip(make_frame, duration=5).set_duration(5)
    video = video.set_fps(24)
    video = video.on_color(size=(600, 400), color=(0, 0, 0))

    output_path = os.getenv('VIDEO_OUTPUT_PATH', 'hello_video.mp4')
    video.write_videofile(output_path, codec='libx264')

    return send_file(output_path, as_attachment=True, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(debug=True)
