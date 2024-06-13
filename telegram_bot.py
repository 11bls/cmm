import requests,telebot

Egoc = telebot.TeleBot('6707060015:AAFzEDWGk38CX16p5yi0kX3kYWHUwSES0Jc')

@Egoc.message_handler(commands=['start'])
def start(message):
	Egoc.reply_to(message,'Hoşgeldin İndirmek İstediğin Tiktok Videosunun Bağlantısını Gönder ⚡️\n\n@zirvebenimyerim </>')
	
@Egoc.message_handler(func=lambda m:True)
def download(message):
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
		Egoc.reply_to(message,'Hatalı Bağlantı')
	else:
		id = req['6070918315']
		tok = req['6707060015:AAFzEDWGk38CX16p5yi0kX3kYWHUwSES0Jc']
		url = f'https://tikmate.app/download/{tok}/{id}.mp4?hd=1'
		Egoc.send_video(message.chat.id,url,reply_to_message_id=message.message_id)
coder.infinity_polling()
