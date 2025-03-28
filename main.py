import requests
import telebot
import os

# دریافت توکن ربات از متغیر محیطی
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# کلید API نوسان
API_KEY = 'کلید-API-شما'

def fetch_prices():
    try:
        # درخواست به وب‌سرویس نوسان برای دریافت قیمت‌ها
        response = requests.get(f"http://api.navasan.tech/latest/?api_key={API_KEY}")
        data = response.json()

        # استخراج قیمت‌ها از داده‌های دریافت‌شده
        gold_18_price = data['18ayar']['value']
        ounce_price = data['ounce']['value']
        usd_price = data['usd_sell']['value']
        euro_price = data['eur_sell']['value']
        sekkeh_price = data['sekkeh']['value']

        # ساخت پیام خروجی
        result = (
            f"قیمت طلای ۱۸ عیار: {gold_18_price} تومان\n"
            f"قیمت اونس جهانی: {ounce_price} دلار\n"
            f"قیمت دلار: {usd_price} تومان\n"
            f"قیمت یورو: {euro_price} تومان\n"
            f"قیمت سکه امامی: {sekkeh_price} تومان"
        )
        return result

    except Exception as e:
        return f"خطا در دریافت اطلاعات: {e}"

@bot.message_handler(commands=['start', 'price'])
def send_price(message):
    result = fetch_prices()
    bot.send_message(message.chat.id, result)

bot.polling(none_stop=True, interval=0)
