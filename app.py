import re
from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name,URL

global bot
global TOKEN

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   print(request.get_json())
   print(bot)
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)
   print(update)
   if hasattr(update, "message"):
       chat_id = update.message.chat.id
       msg_id = update.message.message_id
       text = update.message.text.encode('utf-8').decode()
   else:
       chat_id = update.edited_message.chat.id
       msg_id = update.edited_message.message_id
       text = update.edited_message.text.encode('utf-8').decode()
   
   # for debugging purposes only
   print("got text message :", text)

   # the first time you chat with the bot AKA the welcoming message
   if text == "/start":
       # print the welcoming message
       bot_welcome = """
       Welcome to testegaia bot.
       """
       # send the welcoming message
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
   else:
       try:
           if text == "/name":
               first_name = update.message.chat.first_name
               bot.sendMessage(chat_id=chat_id, text=first_name, reply_to_message_id=msg_id)
           elif text=="/fullname":
               first_name = update.message.chat.first_name
               last_name = update.message.chat.last_name
               bot.sendMessage(chat_id=chat_id, text="Your full name is {} {}.".format(first_name, last_name), reply_to_message_id=msg_id)
           elif text == "/meet":
               bot.sendMessage(chat_id=chat_id, text="https://meet.google.com/ssx-daxk-htu")
           elif text == "/commands":
               commands = "You can use the following commands: /name , /fullname , /meet . Enjoy!"
               bot.sendMessage(chat_id=chat_id, text=commands)
           else:
               pass

       except Exception:
           # if things went wrong
           bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)
   return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
   s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
   if s:
       return "webhook setup ok"
   else:
       return "webhook setup failed"

@app.route('/')
def index():
   return '.'
if __name__ == '__main__':
   app.run(threaded=True)