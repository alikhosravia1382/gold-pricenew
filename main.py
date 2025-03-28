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
        gold_18_elem = soup.find("td", string="طلای 18 عیار")
        gold_18_price = gold_18_elem.find_next_sibling("td").text.replace(",", "")
        gold_18_price = float(gold_18_price)

        ounce_elem = soup.find("td", string="انس طلا")
        ounce_price = ounce_elem.find_next_sibling("td").text.replace(",", "")
        ounce_price = float(ounce_price)

        ratio = gold_18_price / ounce_price
        return f"قیمت طلای ۱۸ عیار: {gold_18_price} تومان\nقیمت انس طلا: {ounce_price} دلار\nنسبت: {ratio:.4f}"

    except Exception as e:
        return f"خطا در دریافت اطلاعات: {e}"

@bot.message_handler(commands=['start', 'price'])
def send_price(message):
    result = fetch_prices()
    bot.send_message(message.chat.id, result)

bot.polling()