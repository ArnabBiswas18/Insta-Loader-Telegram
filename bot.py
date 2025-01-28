import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import instaloader
from dotenv import load_dotenv
import os
from io import BytesIO
import requests
from requests.exceptions import Timeout, RequestException

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Instantiate Instaloader
loader = instaloader.Instaloader()

# Command to start the bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! Send me an Instagram link and I will fetch the content for you.')

# Function to download Instagram video
async def download(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    if "instagram.com" not in url:
        await update.message.reply_text("Please provide a valid Instagram link.")
        return

    try:
        # Extract the shortcode from the URL
        shortcode = url.split("/")[-2]

        # Get post object from Instaloader
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        # Get the video URL
        video_url = post.video_url

        # Try to download the video with a timeout
        video_data = None
        try:
            response = requests.get(video_url, timeout=60)  # 60 seconds timeout
            response.raise_for_status()  # Check if request was successful
            video_data = BytesIO(response.content)
        except Timeout:
            await update.message.reply_text("The download is taking too long. Please try again later.")
            return
        except RequestException as e:
            logger.error(f"Request error: {e}")
            await update.message.reply_text("An error occurred while trying to download the video. Please try again.")
            return

        if video_data:
            video_data.seek(0)  # Ensure we're at the start of the BytesIO object
            await update.message.reply_video(video_data, caption="Here's your Instagram content!")
        else:
            await update.message.reply_text("Sorry, the video could not be fetched.")

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        await update.message.reply_text(f"Error occurred: {e}")

# Main function to run the bot
def main():
    # Get the bot token from the .env file
    bot_token = os.getenv('BOT_API_TOKEN')
    if bot_token is None:
        print("Error: BOT_API_TOKEN is not set in the .env file")
        return

    # Create the Application instance
    application = Application.builder().token(bot_token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
