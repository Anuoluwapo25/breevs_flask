import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

app = Flask(__name__)

TOKEN = "TELEGRAM_BOT_TOKEN"

application = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text("Hello! I'm your bot.")

async def echo(update: Update, context):
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

@app.route('/webhook', methods=['POST'])
def webhook():
    # Process incoming updates from Telegram
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)
