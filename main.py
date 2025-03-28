import requests
from bs4 import BeautifulSoup
import telebot
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

def fetch_prices():
    url = "https://www.livedata.ir/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        # استخراج قیمت طلای ۱۸ عیار
        gold_18 = soup.find("span", id="l-sekee")
        gold_18_price = gold_18.text.replace(",", "").strip()
        gold_18_price = float(gold_18_price)

        # استخراج قیمت انس طلا
        ounce = soup.find("span", id="l-ons")
        ounce_price = ounce.text.replace(",", "").strip()
        ounce_price = float(ounce_price)

        ratio = gold_18_price / ounce_price

        return f"قیمت طلای ۱۸ عیار: {gold_18_price} تومان\nقیمت انس جهانی: {ounce_price} دلار\nنسبت: {ratio:.4f}"

    except Exception as e:
        return f"خطا در دریافت اطلاعات: {e}"

@bot.message_handler(commands=['start', 'price'])
def send_price(message):
    result = fetch_prices()
    bot.send_message(message.chat.id, result)

bot.polling(none_stop=True, interval=0)
