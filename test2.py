import requests
import time

# Replace with your actual GitHub API token and Codespace name
API_TOKEN = "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"
CODESPACE_NAME = "fictional-space-doodle-j9x76gvrqwpfqqxr"

def start_codespace(api_token, codespace_name):
    endpoint = f"https://api.github.com/user/codespaces/{codespace_name}/start"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.post(endpoint, headers=headers)
    if response.status_code == 200:
        print("Codespace started successfully.")
        return response.json()
    else:
        print(f"Error starting codespace: {response.text}")
        return None

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

# Start the Codespace
codespace_info = start_codespace(API_TOKEN, CODESPACE_NAME)
if codespace_info:
    print(f"Codespace Info: {codespace_info}")

    # Wait a few seconds to ensure the Codespace is fully up
    time.sleep(10)

    # Check the status of the Codespace
    codespace_status = get_codespace_status(API_TOKEN, CODESPACE_NAME)
    if codespace_status:
        print(f"Codespace Status: {codespace_status}")
