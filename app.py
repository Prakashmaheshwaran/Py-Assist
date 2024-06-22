from flask import Flask, request, jsonify, send_file
from addons.check_work import get_specs, generate_video
from addons.fetchpost import get_published_and_scheduled_posts
from addons.image_upload import fetch_and_upload_image
from youtube_transcript_api import YouTubeTranscriptApi
from requests_oauthlib import OAuth1
import requests

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

@app.route('/yt-transcript', methods=['GET'])
def get_youtube_transcript():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"error": "Video ID is required"}), 400
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript_text = ' '.join([entry['text'] for entry in transcript])
        return jsonify({"transcript": transcript_text})
    except Exception as e:
        return jsonify({"error": "No transcript available"})

@app.route('/post/photo', methods=['POST'])
def post_photo():
    data = request.get_json()
    
    # Extract credentials and endpoint details from JSON payload
    consumer_key = data.get('consumer_key')
    consumer_secret = data.get('consumer_secret')
    access_token = data.get('access_token')
    access_token_secret = data.get('access_token_secret')
    blog_name = data.get('blog_name')
    image_url = data.get('image_url')
    caption = data.get('caption', '')
    
    # Tumblr API endpoints
    base_url = f'https://api.tumblr.com/v2/blog/{blog_name}.tumblr.com'
    
    # OAuth1 authentication setup
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)

    # Parameters for the photo post
    params = {
        'type': 'photo',
        'caption': caption,
        'source': image_url,
        # Additional optional parameters can be added here
    }
    
    post_url = f'{base_url}/post'
    response = requests.post(post_url, auth=auth, data=params)
    
    if response.status_code == 201:
        return jsonify({'message': 'Photo posted successfully'}), 201
    else:
        return jsonify({'error': f'Failed to post photo: {response.status_code}'}), response.status_code

@app.route('/post/video', methods=['POST'])
def post_video():
    data = request.get_json()
    
    # Extract credentials and endpoint details from JSON payload
    consumer_key = data.get('consumer_key')
    consumer_secret = data.get('consumer_secret')
    access_token = data.get('access_token')
    access_token_secret = data.get('access_token_secret')
    blog_name = data.get('blog_name')
    video_url = data.get('video_url')
    caption = data.get('caption', '')
    
    # Tumblr API endpoints
    base_url = f'https://api.tumblr.com/v2/blog/{blog_name}.tumblr.com'
    
    # OAuth1 authentication setup
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)

    # Parameters for the video post
    params = {
        'type': 'video',
        'caption': caption,
        'embed': video_url,
        # Additional optional parameters can be added here
    }
    
    post_url = f'{base_url}/post'
    response = requests.post(post_url, auth=auth, data=params)
    
    if response.status_code == 201:
        return jsonify({'message': 'Video posted successfully'}), 201
    else:
        return jsonify({'error': f'Failed to post video: {response.status_code}'}), response.status_code

@app.route('/post/link', methods=['POST'])
def post_link():
    data = request.get_json()
    
    # Extract credentials and endpoint details from JSON payload
    consumer_key = data.get('consumer_key')
    consumer_secret = data.get('consumer_secret')
    access_token = data.get('access_token')
    access_token_secret = data.get('access_token_secret')
    blog_name = data.get('blog_name')
    link_url = data.get('link_url')
    title = data.get('title', '')
    description = data.get('description', '')
    
    # Tumblr API endpoints
    base_url = f'https://api.tumblr.com/v2/blog/{blog_name}.tumblr.com'
    
    # OAuth1 authentication setup
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)

    # Parameters for the link post
    params = {
        'type': 'link',
        'url': link_url,
        'title': title,
        'description': description,
        # Additional optional parameters can be added here
    }
    
    post_url = f'{base_url}/post'
    response = requests.post(post_url, auth=auth, data=params)
    
    if response.status_code == 201:
        return jsonify({'message': 'Link posted successfully'}), 201
    else:
        return jsonify({'error': f'Failed to post link: {response.status_code}'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
