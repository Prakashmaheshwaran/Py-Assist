from requests_oauthlib import OAuth1Session

# Replace these with your actual consumer key and secret
consumer_key = 'GBRLSnn91vpvO6X2PFH17mt9CV2ur0Yxkv8EEWBOucnLu34Yf6'
consumer_secret = 'Ex7ufUUEjbcJPd3bfQBOkGU7QESB3P7wJqzsnYlc8Qq7jQva6o'

# Tumblr OAuth URLs
request_token_url = 'https://www.tumblr.com/oauth/request_token'
authorize_url = 'https://www.tumblr.com/oauth/authorize'
access_token_url = 'https://www.tumblr.com/oauth/access_token'

# Create OAuth1Session instance
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

# Step 1: Fetch request token
fetch_response = oauth.fetch_request_token(request_token_url)

request_token = fetch_response.get('oauth_token')
request_token_secret = fetch_response.get('oauth_token_secret')

print(f"Request Token: {request_token}")
print(f"Request Token Secret: {request_token_secret}")

# Step 2: Direct user to Tumblr's authorization URL
authorization_url = oauth.authorization_url(authorize_url)

print(f"Please go here and authorize: {authorization_url}")

# After the user authorizes the app, they will be redirected back with oauth_verifier
oauth_verifier = input('Paste the oauth_verifier here: ')

# Step 3: Exchange request token for access token
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=request_token,
    resource_owner_secret=request_token_secret,
    verifier=oauth_verifier
)

access_token_response = oauth.fetch_access_token(access_token_url)

access_token = access_token_response.get('oauth_token')
access_token_secret = access_token_response.get('oauth_token_secret')

print(f"Access Token: {access_token}")
print(f"Access Token Secret: {access_token_secret}")

# Now you can use access_token and access_token_secret to make authenticated requests to Tumblr API
