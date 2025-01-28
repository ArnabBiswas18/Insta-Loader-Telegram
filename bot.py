import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Token from BotFather (make sure you set the token in .env)
TOKEN = os.getenv('BOT_API_TOKEN')

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define command handler for /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot. Send me a link and I\'ll process it for you.')

# Define a function to handle regular messages
def handle_message(update: Update, context: CallbackContext) -> None:
    # Check if message contains a link (you can improve this as needed)
    if update.message.entities:
        for entity in update.message.entities:
            if entity.type == 'url':
                # Here you can add your logic to process the URL and send the file or response
                update.message.reply_text(f'Processing the link: {update.message.text}')
                # You can replace this with actual download and file sending logic
                return
    update.message.reply_text('Send me a link to process.')

def main() -> None:
    """Start the bot."""
    # Check if TOKEN is loaded from environment variables
    if not TOKEN:
        logger.error('TOKEN is not set. Please add BOT_API_TOKEN to your .env file.')
        return

    # Initialize the Updater with your bot's token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the /start command handler
    dispatcher.add_handler(CommandHandler("start", start))

    # Register the message handler
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling (long polling to receive updates)
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
