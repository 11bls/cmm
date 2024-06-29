import telebot
from pytube import YouTube
from youtubesearchpython import VideosSearch
import os
import time
from datetime import datetime
import requests

TOKEN = '7293032318:AAFAaIOrVT7fwu92LaIjIFhpF1RvyizFW0M'
OWNER_ID = '6377937320'
CHANNEL_USERNAME = '@m3rtw2guvence'

bot = telebot.TeleBot(TOKEN)

# Başlangıç komutu işlevi
@bot.message_handler(commands=['start'])
def start(message):
    greeting_message = get_greeting_message()
    send_welcome_message(message, greeting_message)

# /indir komutu işlevi
@bot.message_handler(commands=['indir'])
def download_music(message):
    query = " ".join(message.text.split()[1:])
    search_and_send_music(bot, message, query)

# Müzik arama ve gönderme işlevi
def search_and_send_music(bot, message, query):
    videosSearch = VideosSearch(query, limit=1)
    result = videosSearch.result()

    if result["result"]:
        video_url = result["result"][0]["link"]

        try:
            yt = YouTube(video_url)
            stream = yt.streams.filter(only_audio=True).first()

            path = stream.download(output_path=".", filename=yt.title)

            search_message = bot.send_message(message.chat.id, f"🔎 İstediğiniz parça aranıyor...")
            
            time.sleep(2)
            bot.delete_message(message.chat.id, search_message.message_id)
            
            search_message = bot.send_message(message.chat.id, f"⏳ İstediğiniz parça indiriliyor.")
            
            time.sleep(2)
            bot.delete_message(message.chat.id, search_message.message_id)

            with open(path, 'rb') as media:
                caption = f"✦ Parça: {yt.title}\n\n✦ İsteyen: {message.from_user.username}"
                bot.send_audio(message.chat.id, media, caption=caption)

            os.remove(path)
        except Exception as e:
            bot.reply_to(message, "İstediğiniz parça bulunamadı 🥲")
    else:
        bot.reply_to(message, "İstediğiniz parça bulunamadı 🥲")

# /reklam komutu işlevi
@bot.message_handler(commands=['reklam'])
def send_advertisement(message):
    if str(message.from_user.id) == OWNER_ID:
        bot.send_message(message.chat.id, "Owner reklam mesajı")

# Başlangıç mesajını hazırlama işlevi
def get_greeting_message():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Günaydın 🥱"
    elif 12 <= current_hour < 17:
        return "İyi öğlenler 🫠"
    elif 17 <= current_hour < 22:
        return "İyi akşamlar 🤤"
    else:
        return "İyi geceler 😴"

# Hoş geldin mesajını gönderme işlevi
def send_welcome_message(message, greeting_message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    button1 = telebot.types.InlineKeyboardButton("Sahibim ❤️‍🩹", url="https://t.me/t5omas")
    button2 = telebot.types.InlineKeyboardButton("Komutlar 💋", callback_data="commands")
    button3 = telebot.types.InlineKeyboardButton("Kanal 😍", url=CHANNEL_USERNAME)
    markup.add(button1, button2, button3)
    bot.reply_to(message, f"{greeting_message} Ben müzik indirme botuyum, beni tercih ettiğiniz için teşekkür ederim.", reply_markup=markup)

# Callback işlevi
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "commands":
        bot.send_message(call.message.chat.id, "🍓 Komutlar;\n/start - Botu Başlatır 💓\n/indir - Müzik indirir 🥰")

# TikTok video indirme işlevi
@bot.message_handler(func=lambda m: True)
def download_tiktok(message):
    if str(message.from_user.id) == OWNER_ID:
        link = message.text
        headers = {
           'authority': 'api.tikmate.app',
           'accept': '*/*',
           'accept-language': 'ar,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
           'cache-control': 'no-cache',
           'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'origin': 'https://tikmate.app',
           'pragma': 'no-cache',
           'referer': 'https://tikmate.app/',
           'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
           'sec-ch-ua-mobile': '?0',
           'sec-ch-ua-platform': '"Windows"',
           'sec-fetch-dest': 'empty',
           'sec-fetch-mode': 'cors',
           'sec-fetch-site': 'same-site',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33',
        }

        data = {
            'url': f'{link}',
        }

        req = requests.post('https://api.tikmate.app/api/lookup', headers=headers, data=data,verify=False).json()
        ok = req['success']
        if ok == False:
            bot.reply_to(message,'Hatalı Bağlantı')
        else:
            id = req['id']
            tok = req['token']
            url = f'https://tikmate.app/download/{tok}/{id}.mp4?hd=1'
            bot.send_video(message.chat.id,url,reply_to_message_id=message.message_id)

# Bot'u çalıştırma
bot.polling(none_stop=True)
