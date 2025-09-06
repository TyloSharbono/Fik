import re, asyncio, threading
from telethon import TelegramClient, events
import telebot

# --- User API (Real User) ---
api_id = 20141517
api_hash = "40705a00a70d2a57757b9c24e6e297af"
phone = "+918538929537"
client = TelegramClient("session", api_id, api_hash)

# --- Bot API (Featured Bot) ---
BOT_TOKEN = "8384695302:AAHUfY9Q8iL2j_4nRnTivsl2C8SgKl6W74Q"
bot = telebot.TeleBot(BOT_TOKEN)

# --- Settings ---
ADMIN_ID = 8009385011
TARGET_CHANNEL = -1002089891838
keywords = ["approved", "charge", "valid", "thank you", "card added", "successful", "added"]
bot_active = False

# --- Login states ---
awaiting_otp = False
awaiting_pass = False


# --- Card Extractor ---
def is_valid_cc_format(card):
    return bool(re.match(r'^\d{15,16}\|\d{2}\|\d{2}\|\d{3}$', card.strip()))

def extract_cards(text):
    cards = []
    x = re.findall(r'\d+', text)
    if len(x) >= 4:
        ccn, mm, yy, cvv = x[0], x[1], x[2], x[3]
        if mm.startswith("2"): mm, yy = yy, mm
        if len(mm) >= 3: mm, yy, cvv = yy, cvv, mm
        if len(yy) == 4: yy = yy[-2:]
        formatted = f"{ccn}|{mm}|{yy}|{cvv}"
        if is_valid_cc_format(formatted):
            cards.append(formatted)
    return cards


# --- Telethon Listener ---
@client.on(events.NewMessage())
async def monitor_messages(event):
    global bot_active
    if not bot_active:
        return
    text = event.raw_text.lower()
    if any(word in text for word in keywords):
        cards = extract_cards(event.raw_text)
        for card in cards:
            await client.send_message(TARGET_CHANNEL, f"💳 {card}")


# --- Bot Commands ---
@bot.message_handler(commands=["login"])
def login_cmd(message):
    global awaiting_otp
    if message.from_user.id != ADMIN_ID:
        return

    async def send_code():
        if not await client.is_connected():
            await client.connect()
        try:
            if await client.is_user_authorized():
                bot.reply_to(message, "✅ Already logged in! Userbot started.")
                threading.Thread(target=run_userbot, daemon=True).start()
                return
            await client.send_code_request(phone)
            bot.reply_to(message, "📩 OTP sent. Please reply with /otp <code>")
            global awaiting_otp
            awaiting_otp = True
        except Exception as e:
            bot.reply_to(message, f"❌ Error sending code: {e}")

    asyncio.get_event_loop().create_task(send_code())

@bot.message_handler(commands=["otp"])
def otp_cmd(message):
    global awaiting_otp, awaiting_pass
    if message.from_user.id != ADMIN_ID or not awaiting_otp:
        return
    code = message.text.replace("/otp", "").strip()

    async def verify():
        global awaiting_pass, awaiting_otp
        try:
            await client.sign_in(phone=phone, code=code)
            bot.reply_to(message, "✅ Login successful! Userbot started.")
            awaiting_otp = False
            threading.Thread(target=run_userbot, daemon=True).start()
        except Exception as e:
            if "password" in str(e).lower():
                awaiting_pass = True
                bot.reply_to(message, "🔒 Account has 2FA. Please send /pass <password>")
            else:
                bot.reply_to(message, f"❌ OTP failed: {e}")

    asyncio.get_event_loop().create_task(verify())

@bot.message_handler(commands=["pass"])
def pass_cmd(message):
    global awaiting_pass
    if message.from_user.id != ADMIN_ID or not awaiting_pass:
        return
    pwd = message.text.replace("/pass", "").strip()

    async def verify_pass():
        global awaiting_pass
        try:
            await client.sign_in(password=pwd)
            bot.reply_to(message, "✅ 2FA successful! Userbot started.")
            awaiting_pass = False
            threading.Thread(target=run_userbot, daemon=True).start()
        except Exception as e:
            bot.reply_to(message, f"❌ Password failed: {e}")

    asyncio.get_event_loop().create_task(verify_pass())


@bot.message_handler(commands=["start"])
def start_cmd(message):
    global bot_active
    if message.from_user.id != ADMIN_ID:
        return
    bot_active = True
    bot.reply_to(message, "✅ Monitoring started!")

@bot.message_handler(commands=["stop"])
def stop_cmd(message):
    global bot_active
    if message.from_user.id != ADMIN_ID:
        return
    bot_active = False
    bot.reply_to(message, "🛑 Monitoring stopped!")

@bot.message_handler(commands=["key"])
def add_keywords(message):
    global keywords
    if message.from_user.id != ADMIN_ID:
        return
    new_words = message.text.replace("/key", "").strip().lower().split(",")
    for w in new_words:
        w = w.strip()
        if w and w not in keywords:
            keywords.append(w)
    bot.reply_to(message, f"✅ Keywords updated: {', '.join(keywords)}")

@bot.message_handler(commands=["show"])
def show_keywords(message):
    if message.from_user.id != ADMIN_ID:
        return
    bot.reply_to(message, "🔑 Current Keywords:\n" + "\n".join(keywords))

@bot.message_handler(commands=["rms"])
def remove_keyword(message):
    global keywords
    if message.from_user.id != ADMIN_ID:
        return
    word = message.text.replace("/rms", "").strip().lower()
    if word in keywords:
        keywords.remove(word)
        bot.reply_to(message, f"❌ Removed: {word}")
    else:
        bot.reply_to(message, f"⚠️ Not found: {word}")


# --- Run both ---
def run_bot():
    bot.infinity_polling()

def run_userbot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(client.start())
    bot.send_message(ADMIN_ID, "🚀 Userbot running...")
    loop.run_until_complete(client.run_until_disconnected())

# Start bot thread
threading.Thread(target=run_bot, daemon=True).start()

# Notify admin that script is up
bot.send_message(ADMIN_ID, "🤖 Bot started. Send /login to connect your user account.")
