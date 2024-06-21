import os
import requests
import re
import base64
import random
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

def get_wp_credentials(wp_url, wp_username, wp_password):
    AUTH_TOKEN = f"Basic {base64.b64encode(f'{wp_username}:{wp_password}'.encode()).decode()}"
    return AUTH_TOKEN

def fetch_random_image_from_unsplash(keyword):
    UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
    url = "https://api.unsplash.com/search/photos"
    params = {
        'query': keyword,
        'client_id': UNSPLASH_ACCESS_KEY,
        'per_page': 20,
        'orientation': 'landscape'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    images = [img['urls']['regular'] for img in data['results']]
    if not images:
        raise Exception("No images found for the given keyword.")
    return random.choice(images)

def sanitize_filename(filename):
    # Remove any character that is not a letter, number, hyphen, or underscore
    return re.sub(r'[^a-zA-Z0-9-_]', '', filename)

def upload_image_to_wordpress(image_url, keyword, account_suffix, wp_url, wp_username, wp_password):
    try:
        AUTH_TOKEN = get_wp_credentials(wp_url, wp_username, wp_password)
        COMPANY_NAME = account_suffix

        # Download the image
        response = requests.get(image_url)
        if response.status_code != 200:
            print(f"Failed to download image. Status code: {response.status_code}")
            raise Exception(f"Failed to download image. Status code: {response.status_code}")
        
        image = Image.open(BytesIO(response.content))
        
        # Convert the image to PNG in memory
        with BytesIO() as output:
            image.save(output, format="PNG")
            png_data = output.getvalue()

        # Rename the file to keyword and company name
        image_filename = f"{sanitize_filename(keyword)}_{sanitize_filename(account_suffix)}.png"

        # Upload the image to WordPress
        files = {'file': (image_filename, BytesIO(png_data), 'image/png')}
        headers = {'Authorization': AUTH_TOKEN}
        print("Uploading the image to WordPress")
        response = requests.post(f"{wp_url}/wp-json/wp/v2/media", headers=headers, files=files)
        print("Response status code:", response.status_code)
        print("Response content:", response.content)
        response.raise_for_status()
        image_data = response.json()
        image_id = image_data['id']
        image_url = image_data['source_url']
        print(f"Image uploaded with ID: {image_id}, URL: {image_url}")

        # Update metadata
        title = keyword + " - " + COMPANY_NAME
        description = keyword + " - " + COMPANY_NAME
        caption = keyword + " - " + COMPANY_NAME
        alt_text = keyword + " - " + COMPANY_NAME

        media_details = {
            'title': title,
            'description': description,
            'caption': caption,
            'alt_text': alt_text
        }
        headers.update({'Content-Type': 'application/json'})
        response = requests.post(f"{wp_url}/wp-json/wp/v2/media/{image_id}", headers=headers, json=media_details)
        response.raise_for_status()
        print("Media metadata updated for ID:", image_id)

        return image_id, image_url
    except Exception as e:
        print(f"Error in upload process: {e}")
        return None, None

def fetch_and_upload_image(keyword, account_suffix, wp_url, wp_username, wp_password):
    try:
        # Fetch an image URL using the keyword
        try:
            image_url = fetch_random_image_from_unsplash(keyword)
        except Exception:
            image_url = "https://dynoxglobal.com/wp-content/uploads/project-thumb-6-style2-1.png"

        # Upload the fetched image to WordPress
        image_id, uploaded_image_url = upload_image_to_wordpress(image_url, keyword, account_suffix, wp_url, wp_username, wp_password)
        return image_id, uploaded_image_url
    except Exception as e:
        print(f"Error: {e}")
        return None, None