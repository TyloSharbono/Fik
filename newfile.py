import re, asyncio, threading
from telethon import TelegramClient, events
import telebot

# --- Settings ---
API_ID = 20141517
API_HASH = "40705a00a70d2a57757b9c24e6e297af"
BOT_TOKEN = "8384695302:AAHUfY9Q8iL2j_4nRnTivsl2C8SgKl6W74Q"
ADMIN_ID = 8009385011   # apna Telegram user id daalna
TARGET_CHANNEL = -1002089891838

client = TelegramClient("session", API_ID, API_HASH)
bot = telebot.TeleBot(BOT_TOKEN)

phone_number = None
awaiting_otp = False
bot_active = False
keywords = ["approved", "charge", "valid", "thank you", "card added", "successful", "added"]


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


# --- Run both together ---
def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot, daemon=True).start()
print("🤖 Bot started. Send /login <phone_number> to login.")
asyncio.get_event_loop().run_until_complete(client.connect())
asyncio.get_event_loop().run_forever()
