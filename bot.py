from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Get the token from the environment
TOKEN = os.getenv("BOT_API_TOKEN")

# Raise an error if the token is missing
if not TOKEN:
    raise ValueError("BOT_API_TOKEN is missing. Please set it in the .env file.")

# Set up the bot and logging
bot = Bot(TOKEN)

# Set up Flask web server
app = Flask(__name__)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot functions

def start(update, context):
    """Send a welcome message when the bot starts"""
    update.message.reply_text('Hello! Send me an Instagram post or reel link and I will help you download it!')

def help(update, context):
    """Provide help message"""
    update.message.reply_text("Send me an Instagram URL (post/reel) and I will send you the download link.")

def handle_message(update, context):
    """Handle non-command messages"""
    text = update.message.text
    if 'instagram.com' in text:
        # Here you can handle the Instagram link processing
        update.message.reply_text("Processing the Instagram link... Please wait.")
        # Add your logic here for processing the Instagram link and sending the download link
        update.message.reply_text("Here is the download link: <download_link>")
    else:
        update.message.reply_text("Please send a valid Instagram link.")

# Set up Flask route to handle webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = Update.de_json(json_str, bot)
    application.process_update(update)
    return 'OK'

# Ping route to keep the bot alive
@app.route('/ping', methods=['GET'])
def ping():
    """Respond with a 'pong' to keep the bot alive"""
    return "pong"

# Set up Telegram bot
application = Application.builder().token(TOKEN).build()

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Run the Flask app
if __name__ == "__main__":
    # You can specify the port you want here, or let Render automatically pick it
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
