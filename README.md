# Py-Assist

A Flask-based API service that provides WordPress content management, image handling, and video editing capabilities.

## Features

- WordPress post management (publish, schedule, update)
- Image fetching and uploading to WordPress
- Video editing with text overlay effects
- SEO metadata management

## Quick Start

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment variables (optional):
   - `VIDEO_OUTPUT_PATH`: Custom path for edited video output

4. Start the server:
   ```bash
   python app.py
   ```

## API Endpoints

### Get Posts
Retrieve published and scheduled WordPress posts.

```bash
curl -X POST http://127.0.0.1:5000/get-posts \
  -H "Content-Type: application/json" \
  -d '{
    "account_suffix": "example",
    "wp_url": "https://example.com",
    "wp_username": "admin",
    "wp_password": "password"
  }'
```

### Upload Images
Fetch and upload images to WordPress based on keywords.

```bash
curl -X POST http://127.0.0.1:5000/fetch-and-upload-image \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "nature",
    "account_suffix": "example",
    "wp_url": "https://example.com",
    "wp_username": "admin",
    "wp_password": "password"
  }'
```

### Update Posts
Update post media and SEO details.

```bash
curl -X POST http://127.0.0.1:5000/update-post \
  -H "Content-Type: application/json" \
  -d '{
    "account_suffix": "example",
    "post_id": 123,
    "focuskw": "keyword",
    "seo_title": "SEO Title",
    "meta_desc": "Meta Description"
  }'
```

### Edit Videos
Add text overlay to videos.

```bash
curl -X GET http://127.0.0.1:5000/edit-video --output video.mp4
```

## Dependencies

- Flask: Web framework
- moviepy: Video editing
- requests: HTTP client

For a complete list, see `requirements.txt`

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

MIT License
