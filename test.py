import requests

# Replace with your actual GitHub API token and Codespace name
API_TOKEN = "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"
CODESPACE_NAME = "fuzzy-acorn-55wr69jvrx924g5"

def get_codespace_status(api_token, codespace_name):
    endpoint = f"https://api.github.com/user/codespaces/{codespace_name}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting codespace status: {response.text}")
        return None

def access_api(public_url):
    response = requests.get(f"{public_url}/specs")
    if response.status_code == 200:
        print("Specs:", response.json())
    else:
        print(f"Error accessing API: {response.text}")

# Get the Codespace status to retrieve the public URL
codespace_status = get_codespace_status(API_TOKEN, CODESPACE_NAME)
if codespace_status:
    public_url = codespace_status["web_url"]
    print(f"Public URL: {public_url}")
    # Access the API to get specs
    access_api(public_url)
