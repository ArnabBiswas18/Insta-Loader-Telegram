import logging
import os
import instaloader
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.constants import ParseMode
from dotenv import load_dotenv
from flask import Flask, request

# Load environment variables
load_dotenv()
TOKEN = os.getenv('BOT_API_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # Your Render or hosting URL

# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Instaloader
loader = instaloader.Instaloader()

# Bot logic
async def start(update: Update, context) -> None:
    await update.message.reply_text("Hello! Send me an Instagram link to get started.")

async def handle_message(update: Update, context) -> None:
    message_text = update.message.text
    if "instagram.com" in message_text:
        try:
            await update.message.reply_text(f"Processing the link: {message_text}")
            # Process the Instagram link
            post = instaloader.Post.from_shortcode(loader.context, message_text.split("/")[-2])
            if post.is_video:
                await update.message.reply_video(post.url)
            else:
                await update.message.reply_photo(post.url)
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")
            logger.error(f"Error processing link {message_text}: {e}")
    else:
        await update.message.reply_text("Please send a valid Instagram link.")

# Initialize bot application
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Flask routes for webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    """Receive updates from Telegram."""
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "OK", 200

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Set the Telegram webhook."""
    success = application.bot.set_webhook(WEBHOOK_URL + "/webhook")
    if success:
        return "Webhook set successfully!", 200
    else:
        return "Failed to set webhook.", 400

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return "Bot is running!", 200

# Start Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
