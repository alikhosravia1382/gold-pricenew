import requests
import telebot
import os

# دریافت توکن ربات از متغیر محیطی
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

def fetch_prices():
    try:
        # درخواست به وب‌سرویس BRS API برای دریافت قیمت‌ها
        response = requests.get("https://brsapi.ir/Api/Market/Gold.php")
        data = response.json()

        # استخراج قیمت طلای ۱۸ عیار و اونس جهانی
        gold_18_price = data['gram18']
        ounce_price = data['ounce']

        # محاسبه نسبت قیمت طلای ۱۸ عیار به اونس جهانی
        ratio = gold_18_price / ounce_price

        # ساخت پیام خروجی
        result = (
            f"قیمت طلای ۱۸ عیار: {gold_18_price} تومان\n"
            f"قیمت اونس جهانی: {ounce_price} دلار\n"
            f"نسبت قیمت طلای ۱۸ عیار به اونس جهانی: {ratio:.4f}"
        )
        return result

    except Exception as e:
        return f"خطا در دریافت اطلاعات: {e}"

@bot.message_handler(commands=['start', 'price'])
def send_price(message):
    result = fetch_prices()
    bot.send_message(message.chat.id, result)

bot.polling()
