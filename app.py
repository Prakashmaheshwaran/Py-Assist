from flask import Flask, request, jsonify
import random
from addons.specs import get_specs  # Import the get_specs function
from addons.image_fetcher import fetch_images_with_retries  # Import the image fetching function

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
        images = fetch_images_with_retries(keyword)
        if images:
            selected_image = random.choice(images)  # Select one image randomly
            return jsonify({"url": selected_image})
        else:
            return jsonify({"error": "No images found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
