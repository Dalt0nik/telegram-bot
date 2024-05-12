from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import urllib3
import requests
import validators
import io


# Functions to read secret token from file
def read_token():
    with open('token.txt', 'r') as file:
        return file.read().strip()

# Read the token from file
TOKEN = read_token()


# Dictionary to store the state of each user
user_states = {}

# Functions to control states of users

def set_user_state(chat_id, state):
    user_states[chat_id] = state

def clear_user_state(chat_id):
    user_states.pop(chat_id, None)

def get_user_state(chat_id):
    return user_states.get(chat_id)




# Functions to handle handle command messages

# Function to handle the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome to the image processing bot! Type /help to see the available commands.')

# Function to handle the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Commands:\nType /process_image to process an image.')

# Function to handle the /process_image command
async def process_image_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    set_user_state(update.effective_chat.id, 'awaiting_url')
    await update.message.reply_text('Send me an image url to process.')

# Function to handle the /cancel command for processing an image
async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_state = get_user_state(update.effective_chat.id)
    if user_state == 'awaiting_url':
        clear_user_state(update.effective_chat.id)
        await update.message.reply_text('Image processing canceled.')
    else:
        await update.message.reply_text("No active image processing to cancel.")



# Functions to handle non-command messages to handle image URLs

# Function to handle image URLs
async def handle_url_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_state = get_user_state(update.effective_chat.id)
    if user_state == 'awaiting_url':
        url = update.message.text
        if validators.url(url) and (url.endswith('.jpg') or url.endswith('.png') or url.endswith('.jpeg')):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    await update.message.reply_text('Image URL is valid. Processing the image...')
                    image_bytes = io.BytesIO(response.content)
                    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_bytes)
                    clear_user_state(update.effective_chat.id)
                else:
                    await update.message.reply_text('The image URL is not accessible.')
            except Exception as e:
                await update.message.reply_text(f'An error occurred: {str(e)}')
        else:
            await update.message.reply_text('This does not seem to be a valid image URL. Please send a valid URL.')
    else:
        await update.message.reply_text("I'm not sure what to do with this. Type /help for options.")

app = ApplicationBuilder().token(TOKEN).build()



# Handlers for commands

app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("process_image", process_image_command))
app.add_handler(CommandHandler("cancel", cancel_command))


# Handlers for non-command messages to handle image URLs

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url_message))



# Start the bot
app.run_polling()