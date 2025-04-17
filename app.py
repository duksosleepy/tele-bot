import logging
from uuid import uuid4

import httpx
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    InlineQueryHandler,
)

from telebot import bot_token

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}! I'm your Telegram Bot. Type /help for available commands."
    )


async def help_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle the /help command."""
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Display available commands\n"
        "/cat - Get a random cat picture\n"
        "/hello - Get a personal greeting"
    )


async def cat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /cat command - send a random cat picture."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://api.thecatapi.com/v1/images/search"
            )
            response.raise_for_status()
            data = response.json()
            cat_url = data[0]["url"]
            await update.message.reply_photo(cat_url)
        except (httpx.RequestError, KeyError) as e:
            logger.error(f"Error fetching cat image: {e}")
            await update.message.reply_text(
                "Sorry, I couldn't fetch a cat picture right now."
            )


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /hello command - kept from original codebase."""
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")


async def inline_query(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle inline queries."""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Echo",
            input_message_content=InputTextMessageContent(
                query or "Empty query"
            ),
        )
    ]
    await update.inline_query.answer(results)


def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(bot_token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cat", cat))
    application.add_handler(CommandHandler("hello", hello))
    application.add_handler(InlineQueryHandler(inline_query))

    # Start the Bot
    application.run_polling(poll_interval=1.0)


if __name__ == "__main__":
    main()
