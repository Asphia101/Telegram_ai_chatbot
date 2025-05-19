from datetime import datetime
from db import save_chat_history, get_chat_history
from gemini import generate_gemini_response, generate_gemini_response_with_image, generate_gemini_summary
from web_search import search_web
import logging

logger = logging.getLogger(__name__)


async def process_chat_message(user_id, user_input):
    """Handles processing chat messages, searching web, and response generation"""
    if user_input.lower().startswith("/search"):
        search_query = user_input[7:].strip()
        if not search_query:
            return "Please provide a search query after `/search`.", None

        web_results = await search_web(search_query)
        if web_results:
            response = "\n\n".join(web_results)
        else:
            response = "No search results found."
        return response, None
    else:
        bot_response = await generate_gemini_response(user_input)
        if len(bot_response) > 4000:
            bot_response = await generate_gemini_summary(bot_response)
        timestamp = datetime.utcnow()
        save_chat_history(user_id, user_input, bot_response, timestamp)

        return bot_response, None


async def process_image_message(user_id, prompt, image_data):
    """Handles processing image messages"""
    bot_response = await generate_gemini_response_with_image(prompt, image_data)
    if len(bot_response) > 4000:
        bot_response = await generate_gemini_summary(bot_response)
    timestamp = datetime.utcnow()
    save_chat_history(user_id, prompt, bot_response, timestamp)
    return bot_response