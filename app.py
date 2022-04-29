from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('ZWlPACsngCuhH5mKYaaMClbUESPVL/vMvtGgTMZnfu9+oiYB7XVSBCrXTsL05cPxQr+pc579NoPQVTYc7/RXzZHsCjao/RmkFhgrMESrBamzZF8tYM3E+K/b+hCZAtEWVKIikh8OxTi42rt7UFqhzAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('478fec36cf611b6d38a1fc648828534f')

@app.route('/')
def hello():
    return "Hello Flask-Heroku"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()