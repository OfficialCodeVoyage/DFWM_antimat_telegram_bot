import logging
import os
import json
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
import re


load_dotenv()

# Get the bot token from the environment variables
BOT_TOKEN = os.getenv("bot_token")

# Ensure that the bot token is available
if not BOT_TOKEN:
    raise ValueError("No bot token provided. Please set the bot token in the .env file.")

# Path to the JSON file where the bad words list is stored
BAD_WORDS_FILE = 'bad_words.json'

# Load bad words from JSON file
if os.path.exists(BAD_WORDS_FILE):
    with open(BAD_WORDS_FILE, 'r', encoding='utf-8') as file:
        BAD_WORDS = json.load(file)
else:
    BAD_WORDS = []

# Log file to store banned messages
BANNED_MESSAGES_LOG = 'banned_messages.txt'

# List of authorized user IDs
AUTHORIZED_USERS = [717156736, 476191049, 139692499, 964755643]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Алена сказала что МАТ - это Плохо!')


async def detect_bad_words(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text.lower()
    for bad_word in BAD_WORDS:
        # Use regular expression to match whole words only
        if re.search(rf'\b{re.escape(bad_word)}\b', message_text):
            user = update.message.from_user
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Log the message details in the banned_messages.txt file
            with open(BANNED_MESSAGES_LOG, 'a', encoding='utf-8') as log_file:
                log_file.write(
                    f"{timestamp} - User: {user.username} (ID: {user.id}) - Banned Word: {bad_word} - Message: {update.message.text}\n")

            # Send a warning message and delete the detected message
            await update.message.reply_text(f"Лучше спроси у Михалыча когда будет CAMCA! 🥟 (димпл)")
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
            return


async def add_bad_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("Только Алена и Кнопка могут добавлять маты в общий список слов!")
        return

    word_to_add = context.args[0].lower() if context.args else None
    if word_to_add:
        BAD_WORDS.append(word_to_add)
        # Save the updated bad words list to the JSON file
        with open(BAD_WORDS_FILE, 'w', encoding='utf-8') as file:
            json.dump(BAD_WORDS, file, ensure_ascii=False, indent=4)
        await update.message.reply_text(f"Добавлено в список запрещённых слов.")
        await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    else:
        await update.message.reply_text("Необходимо указать слово для добавления. Использование: /addbadword <слово>")


async def main() -> None:
    # Initialize the bot application with the bot token
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addbadword", add_bad_word))
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
