from flask import Flask
from flask import request
from flask import Response
import requests
from stockview import StockView
import telegram
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
import os

TOKEN = os.environ.get("TOKEN")
URL = os.environ.get("URL")

app = Flask(__name__)


bot = telegram.Bot(token=TOKEN)
URL = "https://70c9-139-47-18-90.eu.ngrok.io"


def tel_parse_message(message):
    print("message-->", message)
    try:
        chat_id = message.message.chat_id
        txt = message.message.text
        print("chat_id-->", chat_id)
        print("txt-->", txt)

        return chat_id, txt
    except:
        print("NO text found-->>")


# DEPRECATED BY NOW
# def tel_send_message(chat_id, text):
#     url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
#     payload = {
#         'chat_id': chat_id,
#         'text': text
#     }
#
#     r = requests.post(url, json=payload)
#
#     return r


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # retrieve the message in JSON and then transform it to Telegram object
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        try:
            chat_id, txt = tel_parse_message(update)
            if txt == "/stock":
                update.message.reply_text('Choose an enterprise')
                stock_view = StockView("2")
                for message in stock_view.get_percentage():
                    bot.send_message(chat_id=chat_id, text=message)

            else:
                bot.send_message(chat_id=chat_id, text="from the webhook")
        except:
            print("from index-->")

        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook(URL)
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


if __name__ == '__main__':
    app.run(threaded=True)

# https://api.telegram.org/bot5535320183:AAF_wqhZNEQ5yIqAGwtesGBxtIHrlrLJG9I/setWebhook?url=https://de5b-139-47-18-90.eu.ngrok.io