import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_HOST")
client = MongoClient(MONGO_URI)
db = client["telegram_bot"]
users_collection = db["users"]
chat_history_collection = db["chat_history"]
file_metadata_collection = db["file_metadata"]


def save_user_data(user_data):
    """Saves user data to MongoDB."""
    users_collection.insert_one(user_data)


def update_user_phone(chat_id, phone_number):
    """Updates user's phone number in MongoDB."""
    users_collection.update_one({"chat_id": chat_id}, {"$set": {"phone_number": phone_number}})


def save_chat_history(user_id, user_input, bot_response, timestamp):
    """Saves chat interaction to MongoDB."""
    chat_entry = {
        "user_id": user_id,
        "user_input": user_input,
        "bot_response": bot_response,
        "timestamp": timestamp
    }
    chat_history_collection.insert_one(chat_entry)


def get_chat_history(user_id, limit=10):
    """Fetches chat history for a user from MongoDB."""
    return list(chat_history_collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit))


def save_file_metadata(user_id, file_name, file_type, description, timestamp):
    """Saves file metadata to MongoDB."""
    file_entry = {
        "user_id": user_id,
        "file_name": file_name,
        "file_type": file_type,
        "description": description,
        "timestamp": timestamp
    }
    file_metadata_collection.insert_one(file_entry)

def get_user_analytics():
    """Gets user analytics from MongoDB."""
    total_users = users_collection.count_documents({})
    total_chats = chat_history_collection.count_documents({})
    total_files = file_metadata_collection.count_documents({})

    return {
            "total_users": total_users,
            "total_chats": total_chats,
            "total_files": total_files
        }