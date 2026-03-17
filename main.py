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
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ၂။ Bot Setup
TOKEN = os.environ.get('BOT_TOKEN') 
ADMIN_ID = os.environ.get('ADMIN_ID', '6343475200')
bot = telebot.TeleBot(TOKEN)

# ၃။ ပုံ Link များ
LOGO_IMAGE = "https://raw.githubusercontent.com/noservice8-cmd/AT_Digital_Store_bot/main/Logo.jpg"
CANVA_IMAGE = "https://raw.githubusercontent.com/noservice8-cmd/AT_Digital_Store_bot/main/1.jpg"
ADMIN_IMAGE = "https://raw.githubusercontent.com/noservice8-cmd/AT_Digital_Store_bot/main/Admin.jpg"

# ၄။ Keyboard Menu Function
def get_main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('🛍 ပစ္စည်းများကြည့်ရန်')
    item2 = types.KeyboardButton('💳 ငွေလွှဲအကောင့်များ')
    item3 = types.KeyboardButton('👨‍💻 Admin ဆက်သွယ်ရန်')
    item4 = types.KeyboardButton('🤝 Resell လုပ်လိုသူများ')
    item5 = types.KeyboardButton('🔄 Refresh (ပြန်စတင်ရန်)')
    markup.add(item1)
    markup.add(item2, item3)
    markup.add(item4, item5)
    return markup

def send_menu(message):
    welcome_text = (
        "✨ **AT Digital Store** မှ ကြိုဆိုပါတယ်။\n\n"
        "လူကြီးမင်း ဝယ်ယူလိုသော ဝန်ဆောင်မှုများကို "
        "အောက်ပါ Menu မှတစ်ဆင့် စိတ်ကြိုက် ရွေးချယ်နိုင်ပါပြီ ခင်ဗျာ။"
    )
    try:
        bot.send_photo(message.chat.id, LOGO_IMAGE, caption=welcome_text, reply_markup=get_main_menu(), parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu(), parse_mode='Markdown')

# --- Message Handlers ---

@bot.message_handler(commands=['start', 'refresh'])
def start(message):
    send_menu(message)

@bot.message_handler(func=lambda message: message.text == '🛍 ပစ္စည်းများကြည့်ရန်')
def show_products(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🎨 Canva Pro (Edu) ဝယ်ယူရန်", callback_data="prod_canva"))
    product_text = "✨ **AT Digital Store** မှ လက်ရှိ ရရှိနိုင်သော ဝန်ဆောင်မှုများ"
    bot.send_photo(message.chat.id, LOGO_IMAGE, caption=product_text, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == '👨‍💻 Admin ဆက်သွယ်ရန်')
def contact_admin(message):
    admin_text = (
        "✨ **Admin နှင့်ဆက်သွယ်ပြောဆိုလိုပါက စာရေးသားပေးပို့နိုင်ပါတယ်ခင်ဗျာ။**\n\n"
        "Admin မှ အမြန်ဆုံးပြန်လည်ဆက်သွယ်ပေးပါမယ်ခင်ဗျာ။\n\n"
        "🔗 Admin Account: @kokowphyo"
    )
    try:
        bot.send_photo(message.chat.id, ADMIN_IMAGE, caption=admin_text, parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, admin_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == '💳 ငွေလွှဲအကောင့်များ')
def payment_info(message):
    pay_text = (
        "💳 **ငွေလွှဲရန် အကောင့်**\n\n"
        "💰 **KPay**\n"
        "📱 **09 689 094 369**\n"
        "👤 **Daw Ohn Myint**\n\n"
        "✅ ငွေလွှဲပြီးပါက **ငွေလွှဲပြေစာ (Screenshot)** နှင့် Gmail ကို ပို့ပေးထားပါခင်ဗျာ။"
    )
    bot.send_photo(message.chat.id, LOGO_IMAGE, caption=pay_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == '🤝 Resell လုပ်လိုသူများ')
def resell_info(message):
    resell_text = "🤝 **Resell လုပ်လိုသူများအတွက်**\n\nဝန်ဆောင်မှုများကို တစ်ဆင့်ပြန်လည်ရောင်းချလိုပါက Admin နှင့် တိုက်ရိုက်ဆက်သွယ်ပေးပါရန်။\n\n🔗 Admin: @kokowphyo"
    bot.send_photo(message.chat.id, LOGO_IMAGE, caption=resell_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == '🔄 Refresh (ပြန်စတင်ရန်)')
def refresh_menu(message):
    send_menu(message)

@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    bot.send_message(message.chat.id, "✅ ပြေစာ လက်ခံရရှိပါသည်။ Admin စစ်ဆေးပြီးပါက ပစ္စည်း ပို့ပေးပါမည်။")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(ADMIN_ID, f"📸 **ငွေလွှဲပြေစာ ရောက်လာပါပြီ**\nUser ID: `{message.chat.id}`", parse_mode='Markdown')

@bot.message_handler(commands=['sendkey'])
def send_key_to_user(message):
    if str(message.chat.id) == ADMIN_ID:
        try:
            args = message.text.split(maxsplit=2)
            target_user_id = args[1]
            content = args[2]
            bot.send_message(target_user_id, f"✅ **ပစ္စည်းရောက်ရှိလာပါပြီ**\n\n📩 အချက်အလက်: `{content}`", parse_mode='Markdown')
            bot.reply_to(message, "✅ ပို့ဆောင်ပြီးပါပြီ။")
        except:
            bot.reply_to(message, "❌ ပုံစံ- /sendkey [ID] [စာသား]")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_direct_text(message):
    if str(message.chat.id) == ADMIN_ID:
        return
    
    warning_text = (
        "⚠️ **လူကြီးမင်း ပို့လိုသည်များကို အောက်ပါ ခလုတ်များနှိပ်၍ ပေးပို့ပါရန်။**\n\n"
        "သီးခြားပြောဆိုရန်ရှိပါက **'👨‍💻 Admin ဆက်သွယ်ရန်'** ကို နှိပ်၍ ပြောဆိုနိုင်ပါတယ်ခင်ဗျာ။"
    )
    bot.send_message(message.chat.id, warning_text, reply_markup=get_main_menu())

# --- ပြင်ဆင်လိုက်သည့်အပိုင်း (Canva Detail) ---
@bot.callback_query_handler(func=lambda call: call.data == 'prod_canva')
def canva_detail(call):
    detail_text = (
        "🎨 **Canva EDU account (1 Year) ရပါပြီ**\n\n"
        "➡️ **Price** - 5,000 ks\n"
        "⏰ **Delivery time** - within 12 hours\n\n"
        "👉 ၁၂ နာရီအတွင်း Email Invite ရောက်လာပါလိမ့်မယ်။ ရောက်လာတဲ့အခါ Join ကို နှိပ်ပြီးတော့ Pro Features အကုန်နီးပါး သုံးလိုရပါပြီ။\n\n"
        "👉 မိမိအနေနဲ့ Canva Edu account မဝယ်ယူခင်၊ အရင်ဆုံး Canva မှာ အကောင့်အရင်ဖွင့်ထားဖို လိုအပ်ပါတယ်။ ဝယ်ယူတဲ့အခါမှာ မိမိ Canva အကောင့်ဖွင့်ထားတဲ့ Email မဟုတ်ဘဲ အခြား Email မှားပြီးပိုရင်တော့ တာဝန်မယူပါဘူးခင်ဗျ။\n\n"
        "✅ **Reseller (ပြန်လည်ရောင်းချလိုသူများ)** အနေနဲ့ Admin ဆီမှာ လာရောက်စုံစမ်းဝယ်ယူလို့ရပါပြီ။"
    )
    bot.send_photo(call.message.chat.id, CANVA_IMAGE, caption=detail_text, parse_mode='Markdown')

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
