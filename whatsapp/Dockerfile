# Use an official Node.js runtime as a parent image
FROM node:20-alpine

# Install necessary packages
RUN apk update && apk upgrade && \
    apk add --no-cache \
    chromium \
    nss \
    freetype \
    freetype-dev \
    harfbuzz \
    ca-certificates \
    ttf-freefont

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Expose the port
EXPOSE 3000

# Environment variables to specify the Chromium executable path
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Run the application
CMD ["node", "bot.js"]
