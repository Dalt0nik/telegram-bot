from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import urllib3
import requests


def read_token():
    with open('token.txt', 'r') as file:
        return file.read().strip()

TOKEN = read_token()


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello, {update.effective_user.first_name}')



app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))

app.run_polling()