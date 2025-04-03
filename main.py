import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import schedule
import time
import threading

# تنظیمات اولیه
TOKEN = "7916139042:AAE38udKVTMmHOTIj0TZc_4kxLZjINxN2oY"
GOLD_PRICE_API = "https://api.metals.live/v1/spot/gold"  # یا هر API دیگر

def get_gold_price():
    try:
        response = requests.get(GOLD_PRICE_API)
        data = response.json()
        global_price = data["price"]  # قیمت جهانی طلا (مثلاً به ازای هر اونس)
        iran_18k_price = global_price * 0.75  # تقریباً ۱۸ عیار = ۷۵٪ قیمت جهانی
        return global_price, iran_18k_price
    except:
        return None, None

def send_gold_price(context: CallbackContext):
    global_price, iran_18k_price = get_gold_price()
    if global_price and iran_18k_price:
        ratio = iran_18k_price / global_price
        message = (
            f"💰 قیمت طلای جهانی: {global_price:.2f} دلار/اونس\n"
            f"🏷️ قیمت طلای ۱۸ عیار (تقریبی): {iran_18k_price:.2f}\n"
            f"🔢 نسبت قیمت ۱۸ عیار به جهانی: {ratio:.4f}"
        )
        context.bot.send_message(chat_id=context.job.context, text=message)
    else:
        context.bot.send_message(chat_id=context.job.context, text="خطا در دریافت قیمت طلا!")

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.job_queue.run_repeating(
        send_gold_price,
        interval=1800,  # هر ۱ ساعت ارسال شود (میتوانید تغییر دهید)
        first=0,
        context=chat_id,
    )
    update.message.reply_text("ربات فعال شد! قیمت طلا هر ۱ ساعت ارسال میشود.")

def main():
    updater = Updater(TOKEN)  # حذف use_context=True
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("price", send_price))
    
    updater.start_polling()
    print("ربات در حال اجراست...")
    updater.idle()
if __name__ == "__main__":
    main()

bot.polling(none_stop=True, interval=0)
