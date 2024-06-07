from flask import Flask, request, jsonify
from addons.specs import get_specs  # Import the get_specs function
from addons.image_fetcher import fetch_random_image
from addons.wordpress_helper import upload_image_to_wordpress, fetch_and_upload_image  # Import the functions

app = Flask(__name__)

@app.route('/')
def home():
    return "This is an API page"

@app.route('/specs', methods=['GET'])
def specs_route():
    return get_specs()  # Call the get_specs function

@app.route('/image-search', methods=['GET'])
def image_search():
    keyword = request.args.get('query')
    if not keyword:
        return jsonify({"error": "No query parameter provided"}), 400

    try:
        image_url = fetch_random_image(keyword)
        return jsonify({"url": image_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload-image', methods=['GET'])
def upload_image():
    image_url = request.args.get('image_url')
    keyword = request.args.get('keyword')
    account_suffix = request.args.get('account_suffix')
    if not image_url or not keyword or not account_suffix:
        return jsonify({"error": "Image URL, keyword, or account suffix not provided"}), 400

    try:
        # Upload the image to WordPress
        image_id = upload_image_to_wordpress(image_url, keyword, account_suffix)
        return jsonify({"wp_image_id": image_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/fetch-and-upload-image', methods=['GET'])
def fetch_and_upload_image_endpoint():
    keyword = request.args.get('keyword')
    account_suffix = request.args.get('account_suffix')
    if not keyword or not account_suffix:
        return jsonify({"error": "Keyword or account suffix not provided"}), 400

    try:
        # Fetch and upload the image to WordPress
        image_id = fetch_and_upload_image(keyword, account_suffix)
        return jsonify({"wp_image_id": image_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
