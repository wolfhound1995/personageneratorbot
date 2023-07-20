import telebot
import requests
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv
from telebot import types
def get_from_env(key):
    dotenv_path = join(dirname(__file__), 'token.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)
token = get_from_env('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup2 = types.InlineKeyboardButton("Generate", callback_data="generate")
    markup.add(markup2)
    bot.send_message(message.chat.id, "Press button below to generate new person", reply_markup=markup)
@bot.message_handler()
def echo_all(message):
    if message.text == 'Tip the author':
        bot.send_message(message.chat.id, 'https://www.buymeacoffee.com//wolfhoundt6')
@bot.callback_query_handler(func=lambda call: True)
def test_callback(call): # <- passes a CallbackQuery type object to your function
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    response = requests.get("https://randomuser.me/api/")
    # print(response.content)
    tip = types.KeyboardButton('Tip the author')
    data = json.loads(response.content)
    data_json = data.get('results')
    gender = data_json[0]['gender']
    name = data_json[0]['name']['first'] +" " + data_json[0]['name']['last']
    location = data_json[0]['location']['street']['name']
    building = data_json[0]['location']['street']['number']
    city = data_json[0]['location']['city']
    state = data_json[0]['location']['state']
    country = data_json[0]['location']['country']
    postcode = data_json[0]['location']['postcode']
    email = data_json[0]['email']
    username = data_json[0]['login']['username']
    password = data_json[0]['login']['password']
    age = data_json[0]['dob']['age']
    bday = data_json[0]['dob']['date']
    phone = data_json[0]['phone']
    cell = data_json[0]['cell']
    picture = data_json[0]['picture']['large']
    markup.add(tip)
    bot.send_photo(call.message.chat.id, picture, f"Gender: {gender}\nName: {name}\nLocation: {location}, {building}\nCity: {city}\nState: {state}\nCountry: {country}\nPostcode: {postcode}\nEmail: {email}\nUsername: {username}\nPassword: {password}\nBirthday and age: {bday}, {age} years\nPhones: {phone}, {cell}\n", reply_markup=markup)
    send_welcome(call.message)

bot.infinity_polling()