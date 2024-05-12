from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import urllib3
import requests


def read_token():
    with open('token.txt', 'r') as file:
        return file.read().strip()

TOKEN = read_token()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome to the image processing bot! Type /help to see the available commands.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Commands:\nType /process_image to process an image.')

async def process_image_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Send me an image to process.')

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("process_image", process_image_command))

app.run_polling()