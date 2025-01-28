from telegram.ext import Updater, CommandHandler, MessageHandler, filters  # Updated import

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

# Set up Telegram bot
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Add handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # Updated filter

# Run the Flask app
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
