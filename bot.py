import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from db import save_user_data, update_user_phone, users_collection, get_user_analytics
from handlers import start, handle_start, chat_with_gemini, handle_image

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MONGO_URI = os.getenv("MONGODB_HOST")

# Setup logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)


async def dashboard(update: Update, context: CallbackContext) -> None:
    """Sends bot usage analytics"""
    analytics = get_user_analytics()

    message = f"""
  Bot Analytics Dashboard
  --------------------------
  Total Registered Users: {analytics['total_users']}
  Total Chat Messages: {analytics['total_chats']}
  Total Files Analyzed: {analytics['total_files']}
  """
    await update.message.reply_text(message)


if __name__ == "__main__":
    # Start the bot
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(MessageHandler(filters.CONTACT, handle_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_gemini))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))  # For images
    app.add_handler(MessageHandler(filters.Document.ALL, handle_image))  # For documents

    logging.info("Bot started...")
    app.run_polling()