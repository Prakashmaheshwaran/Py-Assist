import requests

# Replace with your actual GitHub API token
API_TOKEN = "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"

def list_codespaces(api_token):
    endpoint = "https://api.github.com/user/codespaces"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error listing codespaces: {response.text}")
        return None

codespaces = list_codespaces(API_TOKEN)
if codespaces:
    print(f"Total Codespaces: {codespaces['total_count']}")
    for idx, codespace in enumerate(codespaces['codespaces']):
        print(f"{idx + 1}. ID: {codespace['id']}, Name: {codespace['name']}, Repository: {codespace['repository']['full_name']}, State: {codespace['state']}")
else:
    print("No Codespaces found.")
