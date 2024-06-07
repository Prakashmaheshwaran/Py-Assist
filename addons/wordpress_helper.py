import os
import requests
import re
import base64
import tempfile
from dotenv import load_dotenv
from addons.image_fetcher import fetch_random_image

load_dotenv()



def get_wp_credentials(account_suffix):
    
    WP_URL = os.getenv(f"WP_URL_{account_suffix}")
    WP_USERNAME = os.getenv(f"WP_USERNAME_{account_suffix}")
    WP_PASSWORD = os.getenv(f"WP_PASSWORD_{account_suffix}")

    if not WP_URL or not WP_USERNAME or not WP_PASSWORD:
        raise ValueError(f"WordPress credentials for account {account_suffix} are not set properly.")
    
    AUTH_TOKEN = f"Basic {base64.b64encode(f'{WP_USERNAME}:{WP_PASSWORD}'.encode()).decode()}"
    
    return WP_URL, AUTH_TOKEN

def sanitize_filename(filename):
    # Remove any character that is not a letter, number, hyphen, or underscore
    return re.sub(r'[^a-zA-Z0-9-_]', '', filename)

def upload_image_to_wordpress(image_url, keyword, account_suffix):
    try:
        WP_URL, AUTH_TOKEN = get_wp_credentials(account_suffix)
        COMPANY_NAME = os.getenv(f"COMPANY_NAME_{account_suffix}")

        # Create a temporary directory and download the image
        with tempfile.TemporaryDirectory() as tmpdirname:
            sanitized_filename = sanitize_filename(os.path.basename(image_url))
            image_path = os.path.join(tmpdirname, sanitized_filename)
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(image_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
            else:
                print(f"Failed to download image. Status code: {response.status_code}")
                raise Exception(f"Failed to download image. Status code: {response.status_code}")

            # Upload the image to WordPress
            files = {'file': open(image_path, 'rb')}
            headers = {'Authorization': AUTH_TOKEN}
            response = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, files=files)
            response.raise_for_status()
            image_id = response.json()['id']
            print("Image uploaded with ID:", image_id)

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

            return image_id
    except Exception as e:
        print(f"Error: {e}")
        return "60855"

def fetch_and_upload_image(keyword, account_suffix):
    try:
        # Fetch an image URL using the keyword
        image_url = fetch_random_image(keyword)
        if image_url == "https://dynoxglobal.com/wp-content/uploads/dynox-global-defualt-blog-thumbnail-yoast-seo.png":
            return "60855"
        
        # Upload the fetched image to WordPress
        image_id = upload_image_to_wordpress(image_url, keyword, account_suffix)
        return image_id
    except Exception as e:
        print(f"Error: {e}")
        return "60855"
