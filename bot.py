import asyncio
import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables from a .env file
load_dotenv()

# Get the bot token from the environment variables
BOT_TOKEN = os.getenv("bot_token")

# Ensure that the bot token is available
if not BOT_TOKEN:
    raise ValueError("No bot token provided. Please set the bot token in the .env file.")

# List of bad words
BAD_WORDS = ["похуй", "блять", "сука"]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Алена сказала что МАТ - это плохо!')

async def detect_bad_words(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text.lower()
    for bad_word in BAD_WORDS:
        if bad_word in message_text:
            await update.message.reply_text(f"Removed {bad_word} - Лучше спроси у михалыча когда будет самса! 🥟 (симпл)")
            return

async def main() -> None:
    # Initialize the bot application with the bot token
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detect_bad_words))

    # Start the bot
    await application.initialize()
    application.run_polling()  # This is a blocking call that will keep the bot running

if __name__ == '__main__':
    try:
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.run(main())
    except RuntimeError as e:
        if str(e) == "This event loop is already running":
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        else:
            raise
