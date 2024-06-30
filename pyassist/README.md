# Project README.md

## Project Overview

This project is a Flask-based API that provides various functionalities related to managing WordPress posts, uploading images, and editing videos. Below are the details of each endpoint along with sample `curl` commands and payload requests.

## Endpoints

### 1. Home

- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns a simple message indicating that this is an API page.
- **Sample `curl` Request**:
  ```bash
  curl -X GET http://127.0.0.1:5000/
  ```

### 2. Get Specs

- **URL**: `/specs`
- **Method**: `GET`
- **Description**: Retrieves specifications of the API.
- **Sample `curl` Request**:
  ```bash
  curl -X GET http://127.0.0.1:5000/specs
  ```

### 3. Get Posts

- **URL**: `/get-posts`
- **Method**: `POST`
- **Description**: Retrieves published and scheduled posts from a WordPress site.
- **Sample `curl` Request**:
  ```bash
  curl -X POST http://127.0.0.1:5000/get-posts -H "Content-Type: application/json" -d '{
    "account_suffix": "example",
    "wp_url": "https://example.com",
    "wp_username": "admin",
    "wp_password": "password"
  }'
  ```

### 4. Fetch and Upload Image

- **URL**: `/fetch-and-upload-image`
- **Method**: `POST`
- **Description**: Fetches an image based on a keyword and uploads it to a WordPress site.
- **Sample `curl` Request**:
  ```bash
  curl -X POST http://127.0.0.1:5000/fetch-and-upload-image -H "Content-Type: application/json" -d '{
    "keyword": "nature",
    "account_suffix": "example",
    "wp_url": "https://example.com",
    "wp_username": "admin",
    "wp_password": "password"
  }'
  ```

### 5. Update Post

- **URL**: `/update-post`
- **Method**: `POST`
- **Description**: Updates the media and SEO details of a WordPress post.
- **Sample `curl` Request**:
  ```bash
  curl -X POST http://127.0.0.1:5000/update-post -H "Content-Type: application/json" -d '{
    "account_suffix": "example",
    "post_id": 123,
    "focuskw": "keyword",
    "seo_title": "SEO Title",
    "meta_desc": "Meta Description"
  }'
  ```

### 6. Edit Video

- **URL**: `/edit-video`
- **Method**: `GET`
- **Description**: Edits a video by adding text moving from right to left over 5 seconds and returns the video file.
- **Sample `curl` Request**:
  ```bash
  curl -X GET http://127.0.0.1:5000/edit-video --output hello_video.mp4
  ```

## Setup and Installation

1. Clone the repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Set the environment variable `VIDEO_OUTPUT_PATH` if needed.
4. Run the Flask application using `python app.py`.

## Environment Variables

- `VIDEO_OUTPUT_PATH`: Path to save the edited video file (default is `hello_video.mp4`).

## Dependencies

- Flask
- moviepy
- requests
- Other dependencies can be found in `requirements.txt`.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
