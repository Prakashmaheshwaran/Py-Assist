import requests
import base64

def get_wp_credentials(wp_url, wp_username, wp_password):
    AUTH_TOKEN = f"Basic {base64.b64encode(f'{wp_username}:{wp_password}'.encode()).decode()}"
    return wp_url, AUTH_TOKEN

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

def get_published_and_scheduled_posts(account_suffix, wp_url, wp_username, wp_password):
    try:
        wp_url, auth_token = get_wp_credentials(wp_url, wp_username, wp_password)
        
        published_posts = fetch_posts('publish', wp_url, auth_token)
        scheduled_posts = fetch_posts('future', wp_url, auth_token)
        all_posts = published_posts + scheduled_posts
        
        formatted_posts = format_posts(all_posts, wp_url)
        return formatted_posts
    except Exception as e:
        return f"An error occurred: {e}"