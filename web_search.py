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


async def search_web(query, num_results=3):
    """Searches the web using Google Custom Search API and provides an AI summary."""
    try:
        service = build("customsearch", "v1", developerKey=GOOGLE_SEARCH_API_KEY)
        response = service.cse().list(q=query, cx=GOOGLE_SEARCH_ENGINE_ID, num=num_results).execute()

        results = []
        if "items" in response:
             combined_text = ""
             for item in response["items"]:
                 title = item.get("title", "No Title")
                 link = item.get("link", "No Link")
                 snippet = item.get("snippet", "No Snippet")
                 results.append(f"**{title}**\n{snippet}\n{link}")
                 combined_text += title + " " + snippet + " "

             summary = await generate_gemini_summary(combined_text)
             results.insert(0,f"**Summary:**\n {summary}\n\n")
             return results
        else:
            return []
    except Exception as e:
         logger.error(f"Error during web search {e}")
         return []