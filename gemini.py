import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging
from PIL import Image
import io

logger = logging.getLogger(__name__)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash") #channging the api key to the free one
model_vision = genai.GenerativeModel('gemini-1.5-flash') # Changed the model name


async def generate_gemini_response(prompt):
        """Sends a prompt to the Gemini model and gets a response."""
        try:
            response = await model.generate_content_async(prompt)
            return response.text
        except Exception as e:
           logger.error(f"Error with Gemini API: {e}")
           return "Error with gemini api: I'm having trouble processing your request at the moment. Please try again later."


async def generate_gemini_response_with_image(prompt, image_data):
    """Sends a prompt and image to the Gemini model and gets a response."""
    try:
        image = Image.open(io.BytesIO(image_data))
        response = await model_vision.generate_content_async([prompt, image])
        return response.text
    except Exception as e:
      logger.error(f"Error with Gemini Vision API: {e}")
      return "I'm having trouble processing your request at the moment. Please try again later."


async def generate_gemini_summary(prompt):
          """Generates a summary of the given content."""
          try:
             response = await model.generate_content_async(f"Summarize the following text: {prompt}")
             return response.text
          except Exception as e:
            logger.error(f"Error during summarization {e}")
            return "I'm having trouble summarizing the content right now. Please try again later"