# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Update the package repository, install curl, and clean up
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Install Ollama with error handling
RUN curl -s https://ollama.ai/install.sh | sh 
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for Ollama host
ENV OLLAMA_HOST=0.0.0.0

# Make port 11434 available to the world outside this container
EXPOSE 11434

# Run Ollama serve
CMD ["ollama", "serve"]
