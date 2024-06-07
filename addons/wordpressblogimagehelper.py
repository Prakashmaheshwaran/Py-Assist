import os
import requests
import re
import base64
import random
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

def get_wp_credentials(account_suffix):
    WP_URL = os.getenv(f"WP_URL_{account_suffix}")
    WP_USERNAME = os.getenv(f"WP_USERNAME_{account_suffix}")
    WP_PASSWORD = os.getenv(f"WP_PASSWORD_{account_suffix}")

    if not WP_URL or not WP_USERNAME or not WP_PASSWORD:
        raise ValueError(f"WordPress credentials for account {account_suffix} are not set properly.")
    
    AUTH_TOKEN = f"Basic {base64.b64encode(f'{WP_USERNAME}:{WP_PASSWORD}'.encode()).decode()}"
    
    return WP_URL, AUTH_TOKEN

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

def convert_image_to_png(image_path):
    with Image.open(image_path) as img:
        png_image_path = image_path.rsplit('.', 1)[0] + '.png'
        img.save(png_image_path, format='PNG')
    return png_image_path

def upload_image_to_wordpress(image_url, keyword, account_suffix):
    try:
        WP_URL, AUTH_TOKEN = get_wp_credentials(account_suffix)
        COMPANY_NAME = os.getenv(f"COMPANY_NAME_{account_suffix}")

        # Download the image
        sanitized_filename = sanitize_filename(os.path.basename(image_url))
        image_path = os.path.join(os.getcwd(), sanitized_filename)
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(image_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            raise Exception(f"Failed to download image. Status code: {response.status_code}")

        # Convert the image to PNG
        png_image_path = convert_image_to_png(image_path)

        # Rename the file to keyword and company name
        renamed_png_image_path = os.path.join(os.getcwd(), f"{sanitize_filename(keyword)}_{sanitize_filename(COMPANY_NAME)}.png")
        os.rename(png_image_path, renamed_png_image_path)

        # Upload the image to WordPress
        with open(renamed_png_image_path, 'rb') as file:
            files = {'file': file}
            headers = {'Authorization': AUTH_TOKEN}
            print("Uploading the image to WordPress")
            response = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, files=files)
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
        response = requests.post(f"{WP_URL}/wp-json/wp/v2/media/{image_id}", headers=headers, json=media_details)
        response.raise_for_status()
        print("Media metadata updated for ID:", image_id)

        # Clean up the downloaded files
        os.remove(image_path)
        os.remove(renamed_png_image_path)

        return image_id, image_url
    except Exception as e:
        print(f"Error in upload process: {e}")
        return None, None

def fetch_and_upload_image(keyword, account_suffix):
    try:
        # Fetch an image URL using the keyword
        try:
            image_url = fetch_random_image_from_unsplash(keyword)
        except Exception:
            image_url = "https://dynoxglobal.com/wp-content/uploads/project-thumb-6-style2-1.png"

        # Upload the fetched image to WordPress
        image_id, uploaded_image_url = upload_image_to_wordpress(image_url, keyword, account_suffix)
        return image_id, uploaded_image_url
    except Exception as e:
        print(f"Error: {e}")
        return None, None
