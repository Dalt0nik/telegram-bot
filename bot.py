from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import urllib3
import requests
import validators


# Functions to read secret token from file
def read_token():
    with open('token.txt', 'r') as file:
        return file.read().strip()

# Read the token from file
TOKEN = read_token()


# Functions to handle handle command messages

# Function to handle the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome to the image processing bot! Type /help to see the available commands.')

# Function to handle the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Commands:\nType /process_image to process an image.')

# Function to handle the /process_image command
async def process_image_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Send me an image url to process.')


# Functions to handle non-command messages to handle image URLs

# Function to handle image URLs
async def handle_url_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    if validators.url(url) and (url.endswith('.jpg') or url.endswith('.png') or url.endswith('.jpeg')):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                await update.message.reply_text('Image URL is valid. Processing...')
                # TO-DO: Add image processing code here
            else:
                await update.message.reply_text('The image URL is not accessible.')
        except Exception as e:
            await update.message.reply_text(f'An error occurred: {str(e)}')
    else:
        await update.message.reply_text('Non-valid image URL. Please send a valid URL.')

app = ApplicationBuilder().token(TOKEN).build()

# Handlers for commands

app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("process_image", process_image_command))

# Handlers for non-command messages to handle image URLs
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url_message))

app.run_polling()