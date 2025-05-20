# Telegram AI Chatbot 

This project is a Telegram bot `@VGeniBot` that leverages Google's Gemini API for natural language processing and MongoDB for data storage. It's designed to provide users with a range of functionalities, including:

- User registration
- Gemini-powered chat
- Image and file analysis
- Web search functionality.

## Features

1.  **User Registration:**
    -   Saves user's first name, username, and chat ID upon their first interaction.
    -   Requests and stores the user's phone number via the Telegram contact button.

2.  **Gemini-Powered Chat:**
    -   Uses the Gemini API to respond to user queries.
    -   Stores the full chat history (user input and bot responses) in MongoDB, including timestamps.

3.  **Image/File Analysis:**
    -   Accepts images and files (e.g., JPG, PNG) and provides a description of their content using Gemini.
    -   Saves file metadata (file name, type, description) in MongoDB.

4.  **Web Search:**
    -   Allows users to perform web searches by typing `/search <query>`.
    -   Returns an AI-generated summary of the search results along with relevant links.

5. **Admin Dashboard:**
    -  Provides users with an admin dashboard that shows statistics about the bot usage. The command to access the dashboard is `/dashboard`

## Technology Stack

*   **Python:** Primary programming language.
*   **Telegram Bot API:** Used for bot development and interaction.
*   **Google Gemini API:** For natural language processing and image analysis.
*   **MongoDB:** For data storage.
*   **python-telegram-bot:**  Python library for Telegram bot interaction.
*   **google-generativeai:** Python library for Google Gemini API access.
*   **pymongo:** Python library for MongoDB interaction.
*   **dotenv:** For secure handling of environment variables.
*  **pillow** : For handling image files
*   **google-api-python-client:**  Python library for Google Custom Search API
*   **beautifulsoup4** : Python library for parsing html content.
*    **requests** : Python library for making web requests

## Setup Instructions

### 1. Prerequisites

   * **Python 3.7+:** Make sure you have a recent version of Python installed.
   *   **Telegram Bot Token:** Obtain your bot token from BotFather on Telegram.
   *   **Google Gemini API Key:** Obtain your API key from Google AI Studio.
   *   **Google Search API Key:** Obtain your API key from Google Cloud Console.
   *  **Google Search Engine ID:** Obtain your ID from Google Custom Search
   *   **MongoDB Atlas:** Set up a free MongoDB Atlas cluster and get your connection URI.
   *   **Create a `.env` file:** Store your secrets securely in a `.env` file in the project directory.

### 2. `.env` File Setup

   1. Create a `.env` file in the same directory as your script and fill in the following details:

         ```env
         TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
         GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
         MONGODB_HOST="YOUR_MONGODB_CONNECTION_URI"
         GOOGLE_SEARCH_API_KEY="YOUR_GOOGLE_SEARCH_API_KEY"
         GOOGLE_SEARCH_ENGINE_ID="YOUR_GOOGLE_SEARCH_ENGINE_ID"
         ```

### 3. Installation

   1.  **Clone the repository** (if applicable):

        ```bash
        git clone <repository_url>
        cd <project_folder>
        ```

   2.  **Install the required Python packages:**

         ```bash
         pip install python-telegram-bot google-generativeai pymongo dotenv pillow google-api-python-client beautifulsoup4 requests
         ```
### 4. Running the Bot
   
   1. Make sure all the settings in the `.env` file are configured correctly.
   2. Run the bot script by executing:
      ```bash
      python bot.py
      ```
   3. The bot should start, and you can start chatting with it through Telegram.

## Project Structure
The project is organized into a modular structure:

- `bot.py`: Main script that initializes the bot and sets up command handlers.
- `db.py`: Contains all database-related configurations and operations.
- `gemini.py`: Contains all code related to the Google Gemini API, including response generation, image analysis, and summarization.
- `handlers.py`: Contains all Telegram handlers for different commands such as /start and /dashboard. It also contains the handling of messages for text, images, and contacts.
- `web_search.py`: Contains all functions related to performing a web search using the Google Custom Search API.
- `bot_logic.py`: Contains the logic of the bot. For example, it calls functions to process a chat message or image.

## Usage
- **Start the Bot**: Send the `/start` command to register.
- **Chat**: Send normal messages to have Gemini respond.
- **Web Search**: Use `/search <query>` to perform a web search.
- **Image/File Description**: Send images or files with a text description (optional) for analysis.
- **Admin Dashboard**: Send /dashboard to get bot usage analytics.

## Testing
- Start a conversation with the bot using a Telegram account.
- Use the `/start` command to register.
- Try sending different types of messages, including text and images.
- Test out the web search using the `/search` command.
- Try the dashboard using the `/dashboard` command.

## Code Quality
- The code is organized in a modular structure.
- Error handling is implemented in all functions.
- The code uses async/await to increase speed and performance.
- All keys are stored safely using environment variables.

## Innovation
The bot implements an admin dashboard to get quick insights on the bot's performance and usage.

## Disclaimer
This bot is provided as an example and may not be suitable for production use without additional testing, error handling, and security measures.

## Contributing
If you want to contribute to this project, please feel free to fork the repository and create a pull request with your changes.

## Contact
If you have any questions or queries please contact me at **<a href="asphiaeariefa@gmail.com" style="color: blue;">asphiaeariefa@gmail.com</a>**.

