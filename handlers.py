import logging
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, ContextTypes
from db import save_user_data, update_user_phone, save_chat_history, get_chat_history, save_file_metadata, \
    users_collection
from gemini import generate_gemini_response, generate_gemini_response_with_image, generate_gemini_summary
from web_search import search_web
from bot_logic import process_chat_message, process_image_message

logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id

    # Check if user already exists
    if users_collection.find_one({"chat_id": chat_id}):
        await update.message.reply_text("You're already registered! 🎉")
        return

    # Save user data in MongoDB
    user_data = {
        "chat_id": chat_id,
        "first_name": user.first_name,
        "username": user.username
    }
    save_user_data(user_data)

    # Ask for phone number
    keyboard = [[KeyboardButton("📞 Share Phone Number", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(f"Hi {user.first_name}! Please share your phone number to complete registration.",
                                    reply_markup=reply_markup)


# async def handle_contact(update: Update, context: CallbackContext) -> None:
#     user = update.message.from_user
#     chat_id = update.message.chat_id
#     phone_number = update.message.contact.phone_number
#
#     # Update user in MongoDB
#     update_user_phone(chat_id, phone_number)
#     await update.message.reply_text("✅ Registration complete! You can now start chatting.")

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    if not user:
        await context.bot.send_message(chat_id, text="User information not available.")
        return

    # Check if the user is already registered
    existing_user = users_collection.find_one({"chat_id": chat_id})

    if not existing_user:
        # Create a new user document
        new_user = {
            "chat_id": chat_id,
            "first_name": user.first_name,
            "username": user.username,
            "phone_number": None,
            "timestamp": datetime.datetime.utcnow()
        }
        users_collection.insert_one(new_user)
        await context.bot.send_message(
            chat_id,
            text=f"Hi {user.first_name}, welcome! I've registered your details.",
        )
        # Request Phone Number
        await context.bot.send_message(
             chat_id,
            "Please share your contact info using the button below to continue.",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("Share Contact", request_contact=True)]],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

    else:
        await context.bot.send_message(
            chat_id,
            text="You are already registered!",
        )

async def chat_with_gemini(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    user_id = update.message.from_user.id

    bot_response, _ = await process_chat_message(user_id, user_input)

    await update.message.reply_text(bot_response, disable_web_page_preview=True)


async def handle_image(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if update.message.photo:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        file_name = file.file_path.split('/')[-1]
        file_type = "photo"
        image_data = await file.download_as_bytearray()
        prompt = update.message.caption if update.message.caption else "What is this image about?"
    elif update.message.document:
        document = update.message.document
        if not document.mime_type.startswith("image"):
            await update.message.reply_text("Please send an image or a file with image")
            return
        file = await context.bot.get_file(document.file_id)
        file_name = document.file_name
        file_type = document.mime_type
        image_data = await file.download_as_bytearray()
        prompt = update.message.caption if update.message.caption else "What is this image about?"
    else:
        await update.message.reply_text("This was not an image")
        return

    bot_response = await process_image_message(user_id, prompt, image_data)
    timestamp = datetime.datetime.utcnow()
    save_file_metadata(user_id, file_name, file_type, bot_response, timestamp)

    await update.message.reply_text(bot_response)