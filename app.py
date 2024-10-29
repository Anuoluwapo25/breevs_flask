import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

app = Flask(__name__)

TOKEN = "TELEGRAM_BOT_TOKEN"
bot = Bot(token=TOKEN)

dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

def start(update, context):
    update.message.reply_text("Hello! I'm your bot.")

def echo(update, context):
    text = update.message.text
    update.message.reply_text(f"You said: {text}")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)
