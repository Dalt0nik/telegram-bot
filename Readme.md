# Telegram Bot - Image Downloader

This Telegram bot processes URLs sent by users, downloads the images if the URLs are valid, and sends them back to the users directly in the chat.

## Setup

### Prerequisites
1. **Docker**: Ensure Docker is installed on your system. If not, download and install Docker from [Docker's official website](https://www.docker.com/products/docker-desktop).

### Configuration
2. Create a `.env` file in the root directory of your project with the following content. Replace `your_telegram_bot_token_here` with your Telegram bot token: `TELEGRAM_TOKEN=your_telegram_bot_token_here`

## Run/Stop
1. Build the Docker Image: `docker-compose up --build`
2. Stopping the Bot: `docker-compose down`

## Features
* Bot supports /help command, to help new users.

* Main feature is image url processing, allowing user to send a url of an image in any of the formats and receive the image itself as a response, if the url is valid.