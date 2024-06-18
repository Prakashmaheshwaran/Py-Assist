import os
import requests
import base64
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

def update_post_media_and_seo(account_suffix, post_id, new_image_id, focuskw, seo_title, meta_desc):
    WP_URL, AUTH_TOKEN = get_wp_credentials(account_suffix)
    headers = {
        'Authorization': f'Basic {AUTH_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'featured_media': new_image_id,
        '_yoast_wpseo_focuskw': focuskw,
        '_yoast_wpseo_title': seo_title,
        '_yoast_wpseo_metadesc': meta_desc
    }
    response = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{post_id}", headers=headers, json=data)
    response.raise_for_status()
    return response.json()

