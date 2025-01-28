import logging
import os
import instaloader
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Token from BotFather (make sure you set the token in .env)
TOKEN = os.getenv('BOT_API_TOKEN')

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Instaloader
L = instaloader.Instaloader()

# Define command handler for /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! I am your bot. Send me an Instagram link, and I\'ll process it for you.')

# Define a function to handle regular messages (process Instagram links)
async def handle_message(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text

    # Check if message contains a link (specifically an Instagram link)
    if "instagram.com" in message_text:
        try:
            # Download the content from Instagram using instaloader
            post = instaloader.Post.from_shortcode(L.context, message_text.split("/")[-2])
            media_url = post.url  # Get the URL of the media (image or video)
            
            # Check the type of content (image or video)
            if post.is_video:
                await update.message.reply_text("Sending you the video...")
                await update.message.reply_video(media_url)
            else:
                await update.message.reply_text("Sending you the image...")
                await update.message.reply_photo(media_url)

        except Exception as e:
            await update.message.reply_text(f"Error occurred: {str(e)}")
            logger.error(f"Error processing link {message_text}: {e}")

    else:
        await update.message.reply_text("Please send a valid Instagram link.")

def main() -> None:
    """Start the bot."""
    # Check if TOKEN is loaded from environment variables
    if not TOKEN:
        logger.error('TOKEN is not set. Please add BOT_API_TOKEN to your .env file.')
        return

    # Initialize the Application with your bot's token
    application = Application.builder().token(TOKEN).build()

    # Register the /start command handler
    application.add_handler(CommandHandler("start", start))

    # Register the message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling (long polling to receive updates)
    application.run_polling()

if __name__ == '__main__':
    main()
