import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# ==========================================
# ၁။ Render အတွက် Web Server (Keep Alive)
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "AT Digital Store Bot is alive and running successfully!"

def run_web():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# ==========================================
# ၂။ Bot Setup & Configuration
# ==========================================
TOKEN = os.environ.get('BOT_TOKEN') 
ADMIN_ID = os.environ.get('ADMIN_ID', '6343475200')

if not TOKEN:
    print("WARNING: BOT_TOKEN is missing. Please set it in Render Environment Variables.")
    bot = None
else:
    bot = telebot.TeleBot(TOKEN)

# ==========================================
# ၃။ ပုံ Link များ (GitHub Raw Links)
# ==========================================
LOGO_IMAGE = "https://raw.githubusercontent.com/noservice8-cmd/AT_Digital_Store_bot/main/Logo.jpg"
CANVA_IMAGE = "https://raw.githubusercontent.com/noservice8-cmd/AT_Digital_Store_bot/main/1.jpg"
ADMIN_IMAGE = "https://raw.githubusercontent.com/noservice8-cmd/AT_Digital_Store_bot/main/Admin.jpg"
HOUSEWIFE_APP_IMAGE = "https://raw.githubusercontent.com/noservice8-cmd/AT_Digital_Store_bot/main/housewife_app_logo.png"

# ==========================================
# ၄။ Keyboard Menu Function
# ==========================================
def get_main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, is_persistent=True)
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

def is_bot_active():
    return bot is not None

# ==========================================
# ၅။ Message Handlers (လုပ်ဆောင်ချက်များ)
# ==========================================

@bot.message_handler(commands=['start', 'refresh'])
def start(message):
    if not is_bot_active(): return
    send_menu(message)

@bot.message_handler(func=lambda message: message.text == '🛍 ပစ္စည်းများကြည့်ရန်')
def show_products(message):
    if not is_bot_active(): return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🌸 'အိမ်ရှင်မ' ဘတ်ဂျက် App ဝယ်ယူရန်", callback_data="prod_housewife"))
    markup.add(types.InlineKeyboardButton(text="🎨 Canva Pro (Edu) ဝယ်ယူရန်", callback_data="prod_canva"))
    product_text = "✨ **AT Digital Store** မှ လက်ရှိ ရရှိနိုင်သော ဝန်ဆောင်မှုများ"
    bot.send_photo(message.chat.id, LOGO_IMAGE, caption=product_text, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == '👨‍💻 Admin ဆက်သွယ်ရန်')
def contact_admin(message):
    if not is_bot_active(): return
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
    if not is_bot_active(): return
    pay_text = (
        "💳 **ငွေလွှဲရန် အကောင့်**\n\n"
        "💰 **KPay**\n"
        "📱 **09 689 094 369**\n"
        "👤 **Daw Ohn Myint**\n\n"
        "✅ ငွေလွှဲပြီးပါက Gmail (သို့) လိုအပ်သည့်အချက်အလက်များကို ပို့ပေးထားပါခင်ဗျာ။"
    )
    bot.send_photo(message.chat.id, LOGO_IMAGE, caption=pay_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == '🤝 Resell လုပ်လိုသူများ')
def resell_info(message):
    if not is_bot_active(): return
    resell_text = "🤝 **Resell လုပ်လိုသူများအတွက်**\n\nဝန်ဆောင်မှုများကို တစ်ဆင့်ပြန်လည်ရောင်းချလိုပါက Admin နှင့် တိုက်ရိုက်ဆက်သွယ်ပေးပါရန်။\n\n🔗 Admin: @kokowphyo"
    bot.send_photo(message.chat.id, LOGO_IMAGE, caption=resell_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == '🔄 Refresh (ပြန်စတင်ရန်)')
def refresh_menu(message):
    if not is_bot_active(): return
    send_menu(message)

@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    if not is_bot_active(): return
    bot.send_message(message.chat.id, "✅ ပြေစာ (သို့) ပုံကို လက်ခံရရှိပါသည်။ Admin စစ်ဆေးပြီးပါက အမြန်ဆုံး အကြောင်းပြန်ပေးပါမည်။")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(ADMIN_ID, f"📸 **ဝယ်သူထံမှ ပုံရောက်လာပါပြီ**\nUser ID: `{message.chat.id}`\nအမည်: {message.from_user.first_name}", parse_mode='Markdown')

@bot.message_handler(commands=['sendkey'])
def send_key_to_user(message):
    if not is_bot_active(): return
    if str(message.chat.id) == ADMIN_ID:
        try:
            args = message.text.split(maxsplit=2)
            if len(args) < 3:
                bot.reply_to(message, "❌ ပုံစံမှားနေပါသည်။ /sendkey [ID] [စာသား] ဟု ရိုက်ပါ ဆရာ။")
                return
            target_user_id = args[1]
            content = args[2]
            bot.send_message(target_user_id, f"✅ **ပစ္စည်းရောက်ရှိလာပါပြီ**\n\n📩 အချက်အလက်: `{content}`", parse_mode='Markdown')
            bot.reply_to(message, "✅ ပို့ဆောင်ပြီးပါပြီ။")
        except:
            bot.reply_to(message, "❌ အမှားအယွင်း ဖြစ်သွားပါသည်။ ပုံစံ- /sendkey [ID] [စာသား]")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_direct_text(message):
    if not is_bot_active(): return
    if str(message.chat.id) == ADMIN_ID:
        return
    
    warning_text = (
        "⚠️ **လူကြီးမင်း ပို့လိုသည်များကို အောက်ပါ ခလုတ်များနှိပ်၍ ပေးပို့ပါရန်။**\n\n"
        "သီးခြားပြောဆိုရန်ရှိပါက **'👨‍💻 Admin ဆက်သွယ်ရန်'** ကို နှိပ်၍ ပြောဆိုနိုင်ပါတယ်ခင်ဗျာ။"
    )
    bot.send_message(message.chat.id, warning_text, reply_markup=get_main_menu())

# ==========================================
# ၆။ Callback Query Handlers (Products Detail)
# ==========================================

# --- အိမ်ရှင်မ App ---
@bot.callback_query_handler(func=lambda call: call.data == 'prod_housewife')
def housewife_detail(call):
    if not is_bot_active(): return
    bot.answer_callback_query(call.id) 

    detail_text = (
        "🌸 **'အိမ်ရှင်မ' ဘတ်ဂျက် App** 🌸\n\n"
        "မိသားစုရဲ့ လစဉ် ဝင်ငွေ၊ ထွက်ငွေတွေကို စာအုပ်ထဲမှာ ရေးမှတ်နေရတာ ရှုပ်ထွေးနေပြီလား? "
        "'အိမ်ရှင်မ' App လေးက သင့်ရဲ့ ငွေကြေးစီမံခန့်ခွဲမှုတွေကို အလွယ်ကူဆုံးနဲ့ အရှင်းလင်းဆုံး ဖြစ်အောင် ကူညီပေးပါလိမ့်မယ်။\n\n"
        "✨ **ဘာတွေ လုပ်ဆောင်ပေးနိုင်လဲ?**\n"
        "💰 ဝင်ငွေ/ထွက်ငွေ အလွယ်တကူ မှတ်သားခြင်း\n"
        "📊 Pie Chart များဖြင့် ရှင်းလင်းစွာ ပြသခြင်း\n"
        "🔒 PIN စနစ်ဖြင့် လုံခြုံမှုပေးခြင်း\n"
        "✅ Offline (အင်တာနက်မလိုဘဲ) သုံးနိုင်ခြင်း\n\n"
        "💎 **Premium Package များ:**\n"
        "🔹 ၆ လ သက်တမ်း - ၁၀,၀၀၀ ကျပ်\n"
        "🔹 ၁ နှစ် သက်တမ်း - ၂၀,၀၀၀ ကျပ်\n"
        "🔹 တစ်သက်တာ (Lifetime) - ၁၀၀,၀၀၀ ကျပ်\n\n"
        "🛒 **ဝယ်ယူရန်:** အောက်ပါ '💳 ဝယ်ယူမည်' ကို နှိပ်ပါ"
    )
    markup = types.InlineKeyboardMarkup()
    
    btn_buy = types.InlineKeyboardButton(text="💳 ဝယ်ယူမည်", callback_data="buy_housewife")
    # ဆရာပေးထားသော App Link အသစ် ထည့်သွင်းထားပါသည်
    btn_app = types.InlineKeyboardButton(text="📥 App ဒေါင်းလုဒ်ဆွဲရန်", url="https://drive.google.com/file/d/15lZC6JSUMBvlFV9oLtMaWW7olH0pfVcG/view?usp=drive_link")
    btn_guide = types.InlineKeyboardButton(text="📖 အသုံးပြုနည်း လမ်းညွှန်", url="https://www.youtube.com/@FuturePlan")
    
    markup.add(btn_buy)
    markup.row(btn_app, btn_guide) 
    
    bot.send_photo(call.message.chat.id, HOUSEWIFE_APP_IMAGE, caption=detail_text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'buy_housewife')
def buy_housewife_step(call):
    if not is_bot_active(): return
    bot.answer_callback_query(call.id) 

    buy_text = (
        "💳 **'အိမ်ရှင်မ' App ဝယ်ယူရန် အဆင့်ဆင့်**\n\n"
        "၁။ မိမိဝယ်ယူလိုသော Package အတွက် ကျသင့်ငွေကို '💳 ငွေလွှဲအကောင့်များ' ခလုတ်တွင် ကြည့်၍ လွှဲပေးပါ။\n\n"
        "၂။ ငွေလွှဲပြီးပါက အောက်ပါ အချက်အလက်များကို ဤ Bot ထံသို့ တိုက်ရိုက် ပေးပို့ပေးပါခင်ဗျာ -\n"
        "   🔸 **ငွေလွှဲပြေစာ (Screenshot)**\n"
        "   🔸 **အသုံးပြုမည့် Device ID**\n"
        "   🔸 **အသုံးပြုလိုသည့်ကာလ** (ဥပမာ - ၆ လ၊ ၁ နှစ်၊ သို့မဟုတ် တစ်သက်တာ)\n\n"
        "၃။ Admin မှ စစ်ဆေးပြီးပါက လူကြီးမင်းထံသို့ **Activation Code** အမြန်ဆုံး ပြန်လည် ပေးပို့ပေးပါမည်။"
    )
    bot.send_message(call.message.chat.id, buy_text, parse_mode='Markdown')

# --- Canva App ---
@bot.callback_query_handler(func=lambda call: call.data == 'prod_canva')
def canva_detail(call):
    if not is_bot_active(): return
    bot.answer_callback_query(call.id)

    detail_text = (
        "🎨 **Canva EDU account (1 Year) ရပါပြီ**\n\n"
        "➡️ **Price** - 5,000 ks\n"
        "⏰ **Delivery time** - within 12 hours\n\n"
        "👉 ၁၂ နာရီအတွင်း Email Invite ရောက်လာပါလိမ့်မယ်။ Join ကို နှိပ်ပြီးတော့ Pro Features အကုန်နီးပါး သုံးလိုရပါပြီ။\n\n"
        "👉 မိမိအနေနဲ့ Canva Edu account မဝယ်ယူခင်၊ အရင်ဆုံး Canva မှာ အကောင့်အရင်ဖွင့်ထားဖို လိုအပ်ပါတယ်။ ဝယ်ယူတဲ့အခါမှာ မိမိ Canva အကောင့်ဖွင့်ထားတဲ့ Email မဟုတ်ဘဲ အခြား Email မှားပြီးပိုရင်တော့ တာဝန်မယူပါဘူးခင်ဗျ။\n\n"
        "✅ **Reseller (ပြန်လည်ရောင်းချလိုသူများ)** အနေနဲ့ Admin ဆီမှာ လာရောက်စုံစမ်းဝယ်ယူလို့ရပါပြီ။"
    )
    bot.send_photo(call.message.chat.id, CANVA_IMAGE, caption=detail_text, parse_mode='Markdown')

# ==========================================
# ၇။ Program စတင်သည့် အပိုင်း (Main Execution)
# ==========================================
if __name__ == "__main__":
    keep_alive()
    if bot:
        print("Bot is successfully running...")
        bot.infinity_polling(timeout=20, long_polling_timeout=10)
