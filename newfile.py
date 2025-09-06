import os, re, asyncio, threading
from telethon import TelegramClient, events
import telebot
from flask import Flask, request

# --- Environment Variables ---
API_ID = "20141517"
API_HASH = "40705a00a70d2a57757b9c24e6e297af"
PHONE = "+918538929537"
PASSWORD = "xitio@2025"
BOT_TOKEN = "8384695302:AAHUfY9Q8iL2j_4nRnTivsl2C8SgKl6W74Q"
ADMIN_ID = 8009385011
WEBHOOK_URL = "https://web-production-99319.up.railway.app/webhook
"  # e.g. https://your-app.up.railway.app/webhook

# --- User API (Real User) ---
client = TelegramClient("session", API_ID, API_HASH)

# --- Bot API (Featured Bot) ---
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- Settings ---
TARGET_CHANNEL = int(os.getenv("TARGET_CHANNEL", "-1001234567890"))
keywords = ["approved", "charge", "valid", "thank you", "card added", "successful", "added"]
bot_active = False
awaiting_otp = False


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
@bot.message_handler(commands=["otp"])
def otp_cmd(message):
    global awaiting_otp
    if message.from_user.id != ADMIN_ID or not awaiting_otp:
        return
    code = message.text.replace("/otp", "").strip()

    async def verify():
        global awaiting_otp
        try:
            await client.sign_in(phone=PHONE, code=code, password=PASSWORD or None)
            bot.reply_to(message, "✅ Login successful! Userbot started.")
            awaiting_otp = False
            threading.Thread(target=run_userbot, daemon=True).start()
        except Exception as e:
            bot.reply_to(message, f"❌ OTP failed: {e}")

    asyncio.get_event_loop().create_task(verify())


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
def run_userbot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(client.start())
    bot.send_message(ADMIN_ID, "🚀 Userbot running...")
    loop.run_until_complete(client.run_until_disconnected())


# --- Auto login process at startup ---
async def auto_login():
    try:
        await client.connect()
        if await client.is_user_authorized():
            bot.send_message(ADMIN_ID, "✅ Already logged in. Userbot starting...")
            threading.Thread(target=run_userbot, daemon=True).start()
        else:
            await client.send_code_request(PHONE)
            global awaiting_otp
            awaiting_otp = True
            bot.send_message(ADMIN_ID, "📩 OTP sent. Please reply with /otp <code>")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ Login error: {e}")


# --- Webhook Setup ---
@app.route("/webhook", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200


# --- Start ---
if __name__ == "__main__":
    # Set webhook
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

    # Start login coroutine
    asyncio.get_event_loop().create_task(auto_login())

    # Run Flask server for webhook
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
