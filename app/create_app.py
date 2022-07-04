from flask import Flask,request
from telebot import types, TeleBot
import pandas as pd


TOKEN = input('YOUR TOKEN:')
bot = TeleBot(TOKEN)
app = Flask(__name__)


#check for user info
def check_user(user_id:int):

    users = pd.read_csv('Users.csv')
    returned_data = users.loc[users.user_id == user_id].user_id.to_list()
    if returned_data == []:
        return True 
    else:
        return False

#save user info
def add_user(user_id,username,first_name,last_name):
    users = pd.read_csv('Users.csv')
    userAdd = pd.DataFrame([{'user_id':user_id,
    "username":username,
    "first_name":first_name,
    "last_name":last_name}])
    users = pd.concat([users, userAdd], ignore_index = True, axis = 0)
    users.to_csv('Users.csv',index=False)
    return "Done"


def create_app():

    app = Flask(__name__)
    @app.route("/")
    def index():
        return "hello world" 



    @bot.message_handler(commands=['start'])
    def start(message):
        
        user_id = message.chat.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        if  check_user(int(user_id)) :
            add_user(user_id,username,first_name,last_name)

            bot.send_message(message.from_user.id,"Welcome " + first_name)
        else:
            bot.send_message(message.from_user.id,"welcome Back " + first_name)

    @app.route('/', methods=['POST'])
    def getMessage():
        json_string = request.get_data().decode('utf-8')
        update = types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200

    @bot.message_handler(commands=['help'])
    def start(message):
        bot.reply_to(message, 'Hellouytt, ' + message.from_user.first_name)


#to set WebHook
    @app.route("/url",methods=["POST"])
    def webhook():
        # url_https = str(request.url_root).replace('http','https')
        url_https = request.form['url']
        print(url_https)
        # print(url_https)
        bot.remove_webhook()
        bot.set_webhook(url=url_https)
        return url_https
        
        
    return app

