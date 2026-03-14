import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# ၁။ Render အတွက် Web Server
app = Flask('')
@app.route('/')
def home():
    return "Digital Shop Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# ၂။ Bot Setup
TOKEN = '8741651961:AAH0uuIJ10pMPveeI27f7hU_WjIGXbbLZUY'
ADMIN_ID = '6343475200' 
bot = telebot.TeleBot(TOKEN)

def send_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('🛒 ပစ္စည်းများ ကြည့်ရန်')
    item2 = types.KeyboardButton('💳 ငွေလွှဲအကောင့်များ')
    item3 = types.KeyboardButton('🔑 Key/Account တောင်းဆိုရန်')
    item4 = types.KeyboardButton('👨‍💻 Admin ဆက်သွယ်ရန်')
    markup.add(item1, item2)
    markup.add(item3, item4)
    bot.send_message(message.chat.id, "✨ AT Digital Store မှ ကြိုဆိုပါတယ်။\nအောက်ပါ Menu မှ တစ်ဆင့် စိတ်ကြိုက်ရွေးချယ်နိုင်ပါပြီ။", reply_markup=markup)

@bot.message_handler(commands=['start', 'refresh'])
def start(message):
    send_menu(message)

# ပစ္စည်းစာရင်း (Inline Button သုံးထားပါတယ်)
@bot.message_handler(func=lambda message: message.text == '🛒 ပစ္စည်းများ ကြည့်ရန်')
def show_products(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🎨 Canva Pro (Edu)", callback_data="prod_canva"))
    # နောင်မှာ တခြားပစ္စည်းတွေ ဒီနေရာမှာ ထပ်တိုးနိုင်ပါတယ်
    
    bot.send_message(message.chat.id, "ရောင်းချပေးနေသော App များ-", reply_markup=markup)

# Canva ကို နှိပ်လိုက်တဲ့အခါ ပြမယ့်စာသား
@bot.callback_query_handler(func=lambda call: call.data == 'prod_canva')
def canva_detail(call):
    detail_text = (
        "🫥 **Canva EDU account (1 Year)**\n\n"
        "➡️ **Price** - 5,000 ks\n\n"
        "⏰ **Delivery time** - within 12 hours\n\n"
        "👉 12 နာရီအတွင်း Email Invite ရောက်လာပါလိမ့်မယ်။ "
        "ရောက်လာတဲ့အခါ Join ကို နှိပ်ပြီးတော့ Pro Features အကုန်နီးပါး သုံးလို့ရပါပြီ။\n\n"
        "👉 မိမိအနေနဲ့ Canva Edu account မဝယ်ယူခင်၊ အရင်ဆုံး Canva မှာ အကောင့်အရင်ဖွင့်ထားဖို့ လိုအပ်ပါတယ်။ "
        "ဝယ်ယူတဲ့အခါမှာ မိမိ Canva အကောင့်ဖွင့်ထားတဲ့ Email မဟုတ်ဘဲ အခြား Email မှားပြီးပို့ရင်တော့ တာဝန်မယူပါဘူးခင်ဗျ။\n\n"
        "✅ **Resell ယူလိုသူများ** အနေနဲ့ Admin ဆီမှာ လာရောက်စုံစမ်းဝယ်ယူလို့ရပါပြီ\n\n"
        "💵 **Payment** 💵 💳\n"
        "Note မှာ \"ငွေပေးချေခြင်း\" လို့သာရေးပေးပါ\n\n"
        "ဆက်သွယ်ဝယ်ယူရန်နှင့် Resell ယူရန်\n"
        "@kokowphyo"
    )
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💳 အခုဝယ်မည် / ငွေလွှဲကြည့်ရန်", callback_data="buy_now"))
    
    bot.send_message(call.message.chat.id, detail_text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'buy_now')
def buy_info(call):
    payment_info = (
        "💳 **ငွေလွှဲရန် အကောင့်များ**\n\n"
        "💰 **KPay / Wave**\n"
        "09450305690\n"
        "U Wai Phyo Paing\n\n"
        "⚠️ Note တွင် 'ငွေပေးချေခြင်း' ဟုသာ ရေးပေးပါ။\n"
        "ငွေလွှဲပြီးပါက ပြေစာ (Screenshot) ကို ဤ Bot ထဲသို့ ပို့ပေးပါခင်ဗျာ။"
    )
    bot.send_message(call.message.chat.id, payment_info, parse_mode='Markdown')

# Admin က ပစ္စည်းပြန်ပို့ရန် Command
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

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_all_text(message):
    if message.text == '💳 ငွေလွှဲအကောင့်များ':
        bot.send_message(message.chat.id, "💳 **ငွေလွှဲရန်အကောင့်**\nKpay/Wave: 09450305690\nအမည်: U Wai Phyo Paing")
    elif message.text == '🔑 Key/Account တောင်းဆိုရန်':
        bot.send_message(message.chat.id, "📸 ငွေလွှဲပြေစာ (Screenshot) နှင့် သင်၏ Email ကို ပို့ပေးထားပါ။")
    elif message.text == '👨‍💻 Admin ဆက်သွယ်ရန်':
        bot.send_message(message.chat.id, "🔗 Admin Contact: @kokowphyo")
    else:
        if str(message.chat.id) != ADMIN_ID:
            bot.send_message(ADMIN_ID, f"📩 **Message အသစ်**\nFrom: `{message.chat.id}`\nText: {message.text}", parse_mode='Markdown')

@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    bot.send_message(message.chat.id, "ပြေစာ လက်ခံရရှိပါသည်။ Admin စစ်ဆေးပြီးပါက ပစ္စည်း ပို့ပေးပါမည်။")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(ADMIN_ID, f"📸 **ငွေလွှဲပြေစာ ရောက်လာပါပြီ**\nUser ID: `{message.chat.id}`", parse_mode='Markdown')

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
