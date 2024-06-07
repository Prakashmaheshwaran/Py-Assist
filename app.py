from flask import Flask, request, jsonify
from addons.specs import get_specs  # Import the get_specs function
from addons.wordpressblogimagehelper import fetch_and_upload_image  # Import the functions

app = Flask(__name__)

@app.route('/')
def home():
    return "This is an API page"

@app.route('/specs', methods=['GET'])
def specs_route():
    return get_specs()  # Call the get_specs function

@app.route('/fetch-and-upload-image', methods=['GET'])
def fetch_and_upload_image_endpoint():
    keyword = request.args.get('keyword')
    account_suffix = request.args.get('account_suffix')
    if not keyword or not account_suffix:
        return jsonify({"error": "Keyword or account suffix not provided"}), 400

    try:
        # Fetch and upload the image to WordPress
        image_id, image_url = fetch_and_upload_image(keyword, account_suffix)
        if image_id is None or image_url is None:
            return jsonify({"error": "Failed to upload image to WordPress"}), 500
        return jsonify({"wp_image_id": image_id, "wp_image_url": image_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
