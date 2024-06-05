from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Access environment variables directly
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

@app.route('/get-image', methods=['GET'])
def get_image():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400

    unsplash_search_url = 'https://api.unsplash.com/search/photos'
    params = {
        'query': keyword,
        'per_page': 1,
        'orientation': 'landscape',
        'client_id': UNSPLASH_ACCESS_KEY
    }
    response = requests.get(unsplash_search_url, params=params)
    if response.status_code == 200:
        image_data = response.json()
        if image_data['results']:
            image_url = image_data['results'][0]['urls']['regular']
            return jsonify({'image_url': image_url})
        else:
            return jsonify({'error': 'No images found'}), 404
    else:
        return jsonify({'error': 'Failed to fetch images'}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
