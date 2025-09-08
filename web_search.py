import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from googleapiclient.discovery import build
from gemini import generate_gemini_summary
import logging

logger = logging.getLogger(__name__)
load_dotenv()

GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

print("GOOGLE_SEARCH_API_KEY:", GOOGLE_SEARCH_API_KEY)  # Debug print
print("GOOGLE_SEARCH_ENGINE_ID:", GOOGLE_SEARCH_ENGINE_ID)  # Debug print

async def search_web(query, num_results=3):
    """Searches the web using Google Custom Search API and provides an AI summary."""
    try:
        print(f"Searching for: {query}")  # Debug print
        service = build("customsearch", "v1", developerKey=GOOGLE_SEARCH_API_KEY)
        response = service.cse().list(q=query, cx=GOOGLE_SEARCH_ENGINE_ID, num=num_results).execute()
        print("Google API response:", response)  # Debug print

        results = []
        if "items" in response:
            combined_text = ""
            for item in response["items"]:
                title = item.get("title", "No Title")
                link = item.get("link", "No Link")
                snippet = item.get("snippet", "No Snippet")
                results.append(f"**{title}**\n{snippet}\n{link}")
                combined_text += title + " " + snippet + " "

            print("Combined text for summary:", combined_text)  # Debug print
            summary = await generate_gemini_summary(combined_text)
            results.insert(0, f"**Summary:**\n {summary}\n\n")
            print("Results to return:", results)  # Debug print
            return results
        else:
            print("No items found in response.")  # Debug print
            return []
    except Exception as e:
        print(f"Error during web search: {e}")  # Debug print
        logger.error(f"Error during web search {e}")
        return []