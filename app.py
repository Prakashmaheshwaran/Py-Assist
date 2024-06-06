from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

UNSPLASH_ACCESS_KEY = 'YOUR_UNSPLASH_ACCESS_KEY'  # Replace this with your Unsplash API Access Key

@app.route('/')
def home():
    return "This is an API page"

@app.route('/image-search', methods=['GET'])
def image_search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query parameter provided"}), 400

    url = "https://api.unsplash.com/search/photos"
    params = {
        'query': query,
        'client_id': UNSPLASH_ACCESS_KEY,
        'per_page': 10
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch images from Unsplash"}), response.status_code

    data = response.json()
    images = [{'id': img['id'], 'url': img['urls']['regular'], 'description': img['description']} for img in data['results']]

    return jsonify(images)

if __name__ == '__main__':
    app.run(debug=True)
