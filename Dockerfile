# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install build-essential, ffmpeg, and ImageMagick
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    ffmpeg \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

# Update ImageMagick policy.xml to allow all operations
RUN sed -i 's/<policy domain="coder" rights="none" pattern="PS"/<policy domain="coder" rights="read|write" pattern="PS"/' /etc/ImageMagick-6/policy.xml && \
    sed -i 's/<policy domain="coder" rights="none" pattern="EPS"/<policy domain="coder" rights="read|write" pattern="EPS"/' /etc/ImageMagick-6/policy.xml && \
    sed -i 's/<policy domain="coder" rights="none" pattern="PDF"/<policy domain="coder" rights="read|write" pattern="PDF"/' /etc/ImageMagick-6/policy.xml && \
    sed -i 's/<policy domain="coder" rights="none" pattern="XPS"/<policy domain="coder" rights="read|write" pattern="XPS"/' /etc/ImageMagick-6/policy.xml && \
    sed -i 's/<policy domain="coder" rights="none" pattern="MSL"/<policy domain="coder" rights="read|write" pattern="MSL"/' /etc/ImageMagick-6/policy.xml && \
    sed -i 's/<policy domain="coder" rights="none" pattern="NULL"/<policy domain="coder" rights="read|write" pattern="NULL"/' /etc/ImageMagick-6/policy.xml && \
    sed -i 's/<policy domain="coder" rights="none" pattern="INLINE"/<policy domain="coder" rights="read|write" pattern="INLINE"/' /etc/ImageMagick-6/policy.xml && \
    sed -i 's/<policy domain="coder" rights="none" pattern="TMP"/<policy domain="coder" rights="read|write" pattern="TMP"/' /etc/ImageMagick-6/policy.xml && \
    sed -i 's/<policy domain="path" rights="none" pattern="@*"/<policy domain="path" rights="read|write" pattern="@*"/' /etc/ImageMagick-6/policy.xml && \
    sed -i 's/<policy domain="coder" rights="none" pattern="PNM"/<policy domain="coder" rights="read|write" pattern="PNM"/' /etc/ImageMagick-6/policy.xml && \
    sed -i 's/<policy domain="coder" rights="none" pattern="PCX"/<policy domain="coder" rights="read|write" pattern="PCX"/' /etc/ImageMagick-6/policy.xml && \
    sed -i 's/<policy domain="coder" rights="none" pattern="PICT"/<policy domain="coder" rights="read|write" pattern="PICT"/' /etc/ImageMagick-6/policy.xml && \
    sed -i 's/<policy domain="coder" rights="none" pattern="PCL"/<policy domain="coder" rights="read|write" pattern="PCL"/' /etc/ImageMagick-6/policy.xml

# Set the environment variable for ImageMagick
ENV IMAGEMAGICK_BINARY=/usr/bin/convert

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
