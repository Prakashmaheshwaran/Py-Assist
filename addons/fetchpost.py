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

def fetch_posts(status, wp_url, auth_token):
    headers = {
        'Authorization': auth_token
    }
    params = {
        'status': status,
        'per_page': 100  # Adjust as needed; maximum is 100 per request
    }
    response = requests.get(f"{wp_url}/wp-json/wp/v2/posts", headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def format_posts(posts, wp_url):
    formatted_posts = ""
    for post in posts:
        title = post['title']['rendered']
        slug_link = f"{wp_url.rstrip('/')}/{post['slug']}"
        formatted_posts += f"{title} - {slug_link}, "
    return formatted_posts.rstrip(', ')

def get_published_and_scheduled_posts(account_suffix):
    try:
        wp_url, auth_token = get_wp_credentials(account_suffix)
        
        published_posts = fetch_posts('publish', wp_url, auth_token)
        scheduled_posts = fetch_posts('future', wp_url, auth_token)
        all_posts = published_posts + scheduled_posts
        
        formatted_posts = format_posts(all_posts, wp_url)
        main_link = "Dynox Global home page - https://dynoxglobal.com/, Dynox global contact page - https://dynoxglobal.com/contact-us/,"
        return main_link + formatted_posts
    except Exception as e:
        return f"An error occurred: {e}"
