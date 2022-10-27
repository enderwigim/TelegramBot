from flask import Flask
from flask import request
from flask import Response
import requests
from stockview import StockView
from telegram import Bot
import os

TOKEN = os.environ.get("TOKEN")

app = Flask(__name__)

stock_view = StockView()
bot = Bot(token=TOKEN)
# URL = "https://de5b-139-47-18-90.eu.ngrok.io"
URL = "https://git.heroku.com/santi-bot.git"


def tel_parse_message(message):
    print("message-->", message)
    try:
        chat_id = message['message']['chat']['id']
        txt = message['message']['text']
        print("chat_id-->", chat_id)
        print("txt-->", txt)

        return chat_id, txt
    except:
        print("NO text found-->>")


def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }

    r = requests.post(url, json=payload)

    return r


def tel_send_image(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': "https://raw.githubusercontent.com/fbsamples/original-coast-clothing/main/public/styles/male-work.jpg",
        'caption': "This is a sample image"
    }

    r = requests.post(url, json=payload)
    return r


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        try:
            chat_id, txt = tel_parse_message(msg)
            if txt == "stock":
                for message in stock_view.get_percentage():
                    tel_send_message(chat_id, message)
            elif txt == "image":
                tel_send_image(chat_id)

            else:
                tel_send_message(chat_id, 'from webhook')
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