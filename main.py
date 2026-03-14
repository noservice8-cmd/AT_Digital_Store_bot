import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# ၁။ Render အတွက် Web Server တည်ဆောက်ခြင်း
app = Flask('')

@app.route('/')
def home():
    return "Digital Shop Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# ၂။ Bot Setup (ဆရာ့ Token ထည့်သွင်းထားသည်)
TOKEN = '8741651961:AAH0uuIJ10pMPveeI27f7hU_WjIGXbbLZUY'
ADMIN_ID = '6343475200' 
bot = telebot.TeleBot(TOKEN)

# ပစ္စည်းစာရင်း
PRODUCTS = {
    "canva": {
        "name": "🎨 Canva Pro (Edu)",
        "price": "၁ လ - ၃၀၀၀ ကျပ် / ၆ လ - ၈၀၀၀ ကျပ်",
        "desc": "ကိုယ့် Account ထဲကို တိုက်ရိုက် Premium သွင်းပေးမှာ ဖြစ်ပါတယ်။"
    }
}

def send_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('🛒 ပစ္စည်းများ ကြည့်ရန်')
    item2 = types.KeyboardButton('💳 ငွေလွှဲအကောင့်များ')
    item3 = types.KeyboardButton('🔑 Key/Account တောင်းဆိုရန်')
    item4 = types.KeyboardButton('👨‍💻 Admin ဆက်သွယ်ရန်')
    markup.add(item1, item2)
    markup.add(item3, item4)
    bot.send_message(message.chat.id, "✨ Digital App Store မှ ကြိုဆိုပါတယ်။", reply_markup=markup)

@bot.message_handler(commands=['start', 'refresh'])
def start(message):
    send_menu(message)

@bot.message_handler(func=lambda message: message.text == '🛒 ပစ္စည်းများ ကြည့်ရန်')
def show_products(message):
    markup = types.InlineKeyboardMarkup()
    for key, item in PRODUCTS.items():
        markup.add(types.InlineKeyboardButton(text=item['name'], callback_data=f"prod_{key}"))
    bot.send_message(message.chat.id, "ရောင်းချပေးနေသော App များ-", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('prod_'))
def product_detail(call):
    product_key = call.data.split('_')[1]
    product = PRODUCTS[product_key]
    detail_text = f"🏷 **{product['name']}**\n\n📝 {product['desc']}\n\n💰 **ဈေးနှုန်း:**\n{product['price']}"
    bot.send_message(call.message.chat.id, detail_text, parse_mode='Markdown')

@bot.message_handler(commands=['sendkey'])
def send_key_to_user(message):
    if str(message.chat.id) == ADMIN_ID:
        try:
            args = message.text.split(maxsplit=2)
            target_user_id = args[1]
            content = args[2]
            msg = f"✅ **လူကြီးမင်း ဝယ်ယူထားသော ပစ္စည်းရောက်ရှိလာပါပြီ**\n\n📩 အချက်အလက်: `{content}`\n\nကျေးဇူးတင်ပါတယ်ခင်ဗျာ 🙏"
            bot.send_message(target_user_id, msg, parse_mode='Markdown')
            bot.reply_to(message, "✅ ပို့ဆောင်ပြီးပါပြီ ဆရာ။")
        except:
            bot.reply_to(message, "❌ ပုံစံမှားနေပါသည်။ /sendkey [ID] [အကြောင်းအရာ]")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_all_text(message):
    if message.text == '💳 ငွေလွှဲအကောင့်များ':
        bot.send_message(message.chat.id, "💳 **ငွေလွှဲရန်အကောင့်**\nKpay/Wave: 09xxxxxxx\nအမည်: U Wai Phyo Paing")
    elif message.text == '🔑 Key/Account တောင်းဆိုရန်':
        bot.send_message(message.chat.id, "📸 ငွေလွှဲပြေစာ (Screenshot) နှင့် သင်၏ Email ကို ပို့ပေးထားပါ။")
    elif message.text == '👨‍💻 Admin ဆက်သွယ်ရန်':
        bot.send_message(message.chat.id, "🔗 Admin Contact: @kokowphyo")
    else:
        if str(message.chat.id) != ADMIN_ID:
            bot.send_message(ADMIN_ID, f"📩 **Message အသစ်**\nFrom: `{message.chat.id}`\nText: {message.text}", parse_mode='Markdown')

@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    bot.send_message(message.chat.id, "ပြေစာ လက်ခံရရှိပါသည်။ ခေတ္တစောင့်ဆိုင်းပေးပါ။")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(ADMIN_ID, f"📸 **ငွေလွှဲပြေစာ ရောက်လာပါပြီ**\nUser ID: `{message.chat.id}`", parse_mode='Markdown')

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
