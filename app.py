import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = f"https://breevs-flask.onrender.com/webhook/{TOKEN}"

application = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text("Welcome! Type /info to get info.")

async def ranking_putaria(update: Update, context):
    await update.message.reply_text("This is the info you requested.")

async def echo_msg(update: Update, context):
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")

async def echo_file(update: Update, context):
    await update.message.reply_text("I received your file!")

async def echo_sticker(update: Update, context):
    await update.message.reply_text("Nice sticker!")

# Add handlers to the application
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("info", ranking_putaria))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_msg))
application.add_handler(MessageHandler(filters.VIDEO | filters.PHOTO | filters.DOCUMENT, echo_file))
application.add_handler(MessageHandler(filters.STICKER, echo_sticker))

async def setup_webhook():
    await application.bot.set_webhook(WEBHOOK_URL)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "ok", 200

if __name__ == '__main__':
    import asyncio
    asyncio.run(setup_webhook())

    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
