import os, re, asyncio, threading
from flask import Flask, request
import telebot
from telethon import TelegramClient, events

# --- Settings ---
API_ID = int(os.getenv("API_ID", "20141517"))
API_HASH = os.getenv("API_HASH", "40705a00a70d2a57757b9c24e6e297af")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8384695302:AAHUfY9Q8iL2j_4nRnTivsl2C8SgKl6W74Q")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8009385011"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://web-production-99319.up.railway.app")

# --- Userbot (Telethon) ---
client = TelegramClient("session", API_ID, API_HASH)
phone_number = None
awaiting_otp = False
bot_active = False
TARGET_CHANNEL = -1002089891838
keywords = ["approved", "charge", "valid", "thank you", "card added", "successful", "added"]

# --- Featured Bot (Telebot) ---
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)


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
    global phone_number, awaiting_otp
    if message.from_user.id != ADMIN_ID:
        return
    try:
        phone_number = message.text.split(" ", 1)[1].strip()
    except:
        bot.reply_to(message, "❌ Usage: /login <phone_number>")
        return

    async def send_code():
        try:
            await client.connect()
            if await client.is_user_authorized():
                bot.reply_to(message, "✅ Already logged in!")
                start_userbot()
                return
            await client.send_code_request(phone_number)
            awaiting_otp = True
            bot.reply_to(message, "📩 OTP sent! Please enter with `/otp <code>`")
        except Exception as e:
            bot.reply_to(message, f"❌ Error: {e}")

    asyncio.get_event_loop().create_task(send_code())


@bot.message_handler(commands=["otp"])
def otp_cmd(message):
    global awaiting_otp
    if message.from_user.id != ADMIN_ID or not awaiting_otp:
        return
    code = message.text.replace("/otp", "").strip()

    async def verify():
        global awaiting_otp
        try:
            await client.sign_in(phone=phone_number, code=code)
            awaiting_otp = False
            bot.reply_to(message, "✅ Login successful! Userbot started.")
            start_userbot()
        except Exception as e:
            bot.reply_to(message, f"❌ OTP failed: {e}")

    asyncio.get_event_loop().create_task(verify())


@bot.message_handler(commands=["start"])
def start_cmd(message):
    global bot_active
    if message.from_user.id == ADMIN_ID:
        bot_active = True
        bot.reply_to(message, "✅ Monitoring started!")


@bot.message_handler(commands=["stop"])
def stop_cmd(message):
    global bot_active
    if message.from_user.id == ADMIN_ID:
        bot_active = False
        bot.reply_to(message, "🛑 Monitoring stopped!")


# --- Helpers ---
def start_userbot():
    def runner():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(client.run_until_disconnected())
    threading.Thread(target=runner, daemon=True).start()


# --- Flask Webhook ---
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def home():
    return "🤖 Bot Running with Webhook", 200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
import os, re, asyncio, threading
from flask import Flask, request
import telebot
from telethon import TelegramClient, events

# --- Settings ---
API_ID = int(os.getenv("API_ID", "20141517"))
API_HASH = os.getenv("API_HASH", "40705a00a70d2a57757b9c24e6e297af")
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://web-production-99319.up.railway.app")

# --- Userbot (Telethon) ---
client = TelegramClient("session", API_ID, API_HASH)
phone_number = None
awaiting_otp = False
bot_active = False
TARGET_CHANNEL = -1002089891838
keywords = ["approved", "charge", "valid", "thank you", "card added", "successful", "added"]

# --- Featured Bot (Telebot) ---
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)


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
    global phone_number, awaiting_otp
    if message.from_user.id != ADMIN_ID:
        return
    try:
        phone_number = message.text.split(" ", 1)[1].strip()
    except:
        bot.reply_to(message, "❌ Usage: /login <phone_number>")
        return

    async def send_code():
        try:
            await client.connect()
            if await client.is_user_authorized():
                bot.reply_to(message, "✅ Already logged in!")
                start_userbot()
                return
            await client.send_code_request(phone_number)
            awaiting_otp = True
            bot.reply_to(message, "📩 OTP sent! Please enter with `/otp <code>`")
        except Exception as e:
            bot.reply_to(message, f"❌ Error: {e}")

    asyncio.get_event_loop().create_task(send_code())


@bot.message_handler(commands=["otp"])
def otp_cmd(message):
    global awaiting_otp
    if message.from_user.id != ADMIN_ID or not awaiting_otp:
        return
    code = message.text.replace("/otp", "").strip()

    async def verify():
        global awaiting_otp
        try:
            await client.sign_in(phone=phone_number, code=code)
            awaiting_otp = False
            bot.reply_to(message, "✅ Login successful! Userbot started.")
            start_userbot()
        except Exception as e:
            bot.reply_to(message, f"❌ OTP failed: {e}")

    asyncio.get_event_loop().create_task(verify())


@bot.message_handler(commands=["start"])
def start_cmd(message):
    global bot_active
    if message.from_user.id == ADMIN_ID:
        bot_active = True
        bot.reply_to(message, "✅ Monitoring started!")


@bot.message_handler(commands=["stop"])
def stop_cmd(message):
    global bot_active
    if message.from_user.id == ADMIN_ID:
        bot_active = False
        bot.reply_to(message, "🛑 Monitoring stopped!")


# --- Helpers ---
def start_userbot():
    def runner():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(client.run_until_disconnected())
    threading.Thread(target=runner, daemon=True).start()


# --- Flask Webhook ---
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def home():
    return "🤖 Bot Running with Webhook", 200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
