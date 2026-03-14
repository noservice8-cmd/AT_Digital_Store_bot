import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# ၁။ Render အတွက် Web Server
app = Flask('')
@app.route('/')
def home():
    return "AT Digital Store Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# ၂။ Bot Setup
TOKEN = '8741651961:AAH0uuIJ10pMPveeI27f7hU_WjIGXbbLZUY'
ADMIN_ID = '6343475200' 
bot = telebot.TeleBot(TOKEN)

# ၃။ ပုံ Link များ
LOGO_IMAGE = "https://raw.githubusercontent.com/noservice8-cmd/AT_Digital_Store_bot/main/Logo.jpg"
CANVA_IMAGE = "https://raw.githubusercontent.com/noservice8-cmd/AT_Digital_Store_bot/main/1.jpg"

# ၄။ ပင်မ Menu ပြသသည့် Function
def send_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('🛍 ပစ္စည်းများကြည့်ရန်')
    item2 = types.KeyboardButton('💳 ငွေလွှဲအကောင့်များ')
    item3 = types.KeyboardButton('👨‍💻 Admin ဆက်သွယ်ရန်')
    item4 = types.KeyboardButton('🔄 Refresh (ပြန်စတင်ရန်)')
    
    markup.add(item1)
    markup.add(item2, item3)
    markup.add(item4)
    
    welcome_text = (
        "✨ **AT Digital Store** မှ ကြိုဆိုပါတယ်။\n\n"
        "လူကြီးမင်း ဝယ်ယူလိုသော ဝန်ဆောင်မှုများကို "
        "အောက်ပါ Menu မှတစ်ဆင့် စိတ်ကြိုက် ရွေးချယ်နိုင်ပါပြီ ခင်ဗျာ။"
    )
    
    try:
        bot.send_photo(message.chat.id, LOGO_IMAGE, caption=welcome_text, reply_markup=markup, parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

# /start သို့မဟုတ် /refresh
@bot.message_handler(commands=['start', 'refresh'])
def start(message):
    send_menu(message)

# 🛍 ပစ္စည်းများကြည့်ရန်
@bot.message_handler(func=lambda message: message.text == '🛍 ပစ္စည်းများကြည့်ရန်')
def show_products(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🎨 Canva Pro (Edu) ဝယ်ယူရန်", callback_data="prod_canva"))
    
    product_text = "✨ **AT Digital Store** မှ လက်ရှိ ရရှိနိုင်သော ဝန်ဆောင်မှုများ"
    
    try:
        bot.send_photo(message.chat.id, LOGO_IMAGE, caption=product_text, reply_markup=markup, parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, product_text, reply_markup=markup, parse_mode='Markdown')

# 💳 ငွေလွှဲအကောင့်များ (Logo ပုံနှင့်အတူပြသခြင်း)
@bot.callback_query_handler(func=lambda call: call.data == 'buy_now')
@bot.message_handler(func=lambda message: message.text == '💳 ငွေလွှဲအကောင့်များ')
def payment_info(message):
    chat_id = message.chat.id if hasattr(message, 'chat') else message.message.chat.id
    pay_text = (
        "💳 **ငွေလွှဲရန် အကောင့်**\n\n"
        "💰 **KPay**\n"
        "📱 **09 689 094 369**\n"
        "👤 **Daw Ohn Myint**\n\n"
        "⚠️ **Note:** တွင် 'ငွေပေးချေခြင်း' ဟုသာ ရေးပေးပါ။\n\n"
        "✅ ငွေလွှဲပြီးပါက **ငွေလွှဲပြေစာ (Screenshot)** ကို ဤ Bot ထဲသို့ တိုက်ရိုက် ပို့ပေးထားပါခင်ဗျာ။"
    )
    try:
        bot.send_photo(chat_id, LOGO_IMAGE, caption=pay_text, parse_mode='Markdown')
    except:
        bot.send_message(chat_id, pay_text, parse_mode='Markdown')

# 👨‍💻 Admin ဆက်သွယ်ရန် (Logo ပုံနှင့်အတူပြသခြင်း)
@bot.message_handler(func=lambda message: message.text == '👨‍💻 Admin ဆက်သွယ်ရန်')
def contact_admin(message):
    admin_text = "🔗 **Admin နှင့် တိုက်ရိုက်ဆက်သွယ်ရန်**\n👉 @kokowphyo"
    try:
        bot.send_photo(message.chat.id, LOGO_IMAGE, caption=admin_text, parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, admin_text, parse_mode='Markdown')

# Canva Detail
@bot.callback_query_handler(func=lambda call: call.data == 'prod_canva')
def canva_detail(call):
    detail_text = (
        "🎨 **Canva EDU account (1 Year)**\n\n"
        "➡️ **Price** - 5,000 ks\n"
        "⏰ **Delivery time** - within 12 hours\n\n"
        "👉 ၁၂ နာရီအတွင်း Email Invite ရောက်လာပါလိမ့်မယ်။\n\n"
        "ဆက်သွယ်ဝယ်ယူရန်နှင့် Resell ယူရန်\n👉 @kokowphyo"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💳 အခုဝယ်မည် / ငွေလွှဲပြေစာ ပို့မည်", callback_data="buy_now"))
    
    try:
        bot.send_photo(call.message.chat.id, CANVA_IMAGE, caption=detail_text, reply_markup=markup, parse_mode='Markdown')
    except:
        bot.send_message(call.message.chat.id, detail_text, reply_markup=markup, parse_mode='Markdown')

# 🔄 Refresh
@bot.message_handler(func=lambda message: message.text == '🔄 Refresh (ပြန်စတင်ရန်)')
def refresh_menu(message):
    send_menu(message)

# Admin Command
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
            bot.reply_to(message, "❌ ပုံစံမှားနေပါသည်။ /sendkey [ID] [စာသား]")

# Handling Text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_all_text(message):
    if str(message.chat.id) != ADMIN_ID:
        bot.send_message(message.chat.id, "📩 လူကြီးမင်း ပို့ထားသော Message ကို လက်ခံရရှိပါသည်။ Admin မှ မကြာမီ ပြန်လည် ဆက်သွယ်ပေးပါမည်။")
        bot.send_message(ADMIN_ID, f"📩 **Message အသစ်**\nFrom: `{message.chat.id}`\nText: {message.text}", parse_mode='Markdown')

# Handling Photo
@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    bot.send_message(message.chat.id, "✅ ပြေစာ လက်ခံရရှိပါသည်။ Admin စစ်ဆေးပြီးပါက ပစ္စည်း ပို့ပေးပါမည်။")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(ADMIN_ID, f"📸 **ငွေလွှဲပြေစာ ရောက်လာပါပြီ**\nUser ID: `{message.chat.id}`", parse_mode='Markdown')

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
