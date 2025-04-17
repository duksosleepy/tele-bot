import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot credentials
bot_token = os.getenv(
    "TELEGRAM_BOT_TOKEN", "here goes your access token from BotFather"
)
bot_user_name = os.getenv("TELEGRAM_BOT_USERNAME", "the username you entered")
url = os.getenv("WEBHOOK_URL", "https://localhost")
