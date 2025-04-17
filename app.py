from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from telebot import bot_token


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")


app = ApplicationBuilder().token(bot_token).build()

app.add_handler(CommandHandler("hello", hello))

app.run_polling()
