# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies, including ImageMagick
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    imagemagick \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Set the environment variable for ImageMagick
ENV IMAGEMAGICK_BINARY /usr/bin/convert
ENV VIDEO_OUTPUT_PATH /app/hello_video.mp4

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]