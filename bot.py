
import os
import telebot
import requests
from datetime import datetime

# البيانات متثبتة وجاهزة
BOT_TOKEN = "8593824542:AAHKYhuXNKLk77qfHhUAu1Evlr_dUEw7sqc"
FOOTBALL_API_KEY = "dd3b58cd63d205097c296c2ecd12eac3"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "⚽ أهلاً بك في بوت أساطير التوقعات! ⚽\n\n"
        "هنا تقدر تشوف ماتشات اليوم وتتوقع نتايجها.\n"
        "اضغط على /matches لعرض مباريات اليوم."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['matches'])
def get_today_matches(message):
    bot.reply_to(message, "⏳ جاري جلب مباريات اليوم من السيرفر...")
    today = datetime.today().strftime('%Y-%m-%d')
    url = f"https://api-sports.io{today}"
    headers = {
        'x-rapidapi-key': FOOTBALL_API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        fixtures = data.get('response', [])
        if not fixtures:
            bot.reply_to(message, "📅 لا توجد مباريات مهمة مجدولة اليوم.")
            return
        response_text = "📅 مباريات اليوم المتاحة للتوقع:\n\n"
        for item in fixtures[:10]:
            home_team = item['teams']['home']['name']
            away_team = item['teams']['away']['name']
            league = item['league']['name']
            status = item['fixture']['status']['long']
            response_text += f"🏆 {league}\n⚔️ {home_team}  ضد  {away_team}\n📢 الحالة: {status}\n-------------------------\n"
        bot.reply_to(message, response_text)
    except Exception as e:
        bot.reply_to(message, "❌ عذراً، حدث خطأ أثناء جلب البيانات.")

if __name__ == "__main__":
    bot.infinity_polling()
