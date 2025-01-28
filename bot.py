from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Set up the bot and logging
TOKEN = os.getenv("BOT_API_TOKEN")
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
        # Here you will handle the download of the Instagram content
        update.message.reply_text("Processing the Instagram link... Please wait.")
        # Call your function to handle the download here (e.g., using Instaloader or requests)
        update.message.reply_text("Here is the download link: <download_link>")
    else:
        update.message.reply_text("Please send a valid Instagram link.")

# Set up Flask route to handle webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = Update.de_json(json_str, bot)
    dispatcher.process_update(update)
    return 'OK'

# Ping route to keep the bot alive
@app.route('/ping', methods=['GET'])
def ping():
    """Respond with a 'pong' to keep the bot alive"""
    return "pong"

# Set up Telegram bot
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Add handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Flask route for basic check
@app.route('/')
def home():
    return "Telegram Bot is running!"

# Run the Flask app
if __name__ == "__main__":
    # Get the port from the environment (Render provides this)
    port = int(os.getenv("PORT", 5000))

    # Run the Flask app to handle the webhook
    app.run(host='0.0.0.0', port=port)
