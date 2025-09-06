import re, asyncio, threading
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
import telebot

# --- Hardcoded credentials ---
api_id = 20141517
api_hash = "40705a00a70d2a57757b9c24e6e297af"
phone = "+918538929537"
BOT_TOKEN = "8384695302:AAHUfY9Q8iL2j_4nRnTivsl2C8SgKl6W74Q"
ADMIN_ID = 8009385011
TARGET_CHANNEL = -1002089891838

keywords = ["approved","charge","valid","thank you","card added","successful","added"]
bot_active = False

# Flags for login
otp_pending = False
pass_pending = False

# --- Telethon client ---
client = TelegramClient("session", api_id, api_hash)
loop = asyncio.get_event_loop()

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

# --- Telethon message listener ---
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

# --- Telebot bot ---
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start_cmd(message):
    global bot_active
    if message.from_user.id != ADMIN_ID:
        return
    bot_active = True
    bot.reply_to(message,"✅ Monitoring started!")

@bot.message_handler(commands=["stop"])
def stop_cmd(message):
    global bot_active
    if message.from_user.id != ADMIN_ID:
        return
    bot_active = False
    bot.reply_to(message,"🛑 Monitoring stopped!")

@bot.message_handler(commands=["otp"])
def otp_cmd(message):
    global otp_pending
    if message.from_user.id != ADMIN_ID:
        return
    otp = message.text.replace("/otp","").strip()
    if not otp:
        bot.reply_to(message,"⚠️ Usage: /otp 12345")
        return
    if otp_pending:
        loop.create_task(complete_otp_login(otp))
        bot.reply_to(message,"🔑 OTP received, completing login...")

@bot.message_handler(commands=["pass"])
def pass_cmd(message):
    global pass_pending
    if message.from_user.id != ADMIN_ID:
        return
    password = message.text.replace("/pass","").strip()
    if not password:
        bot.reply_to(message,"⚠️ Usage: /pass yourpassword")
        return
    if pass_pending:
        loop.create_task(complete_password_login(password))
        bot.reply_to(message,"🔑 Password received, completing 2FA login...")

# --- Telethon login steps ---
async def complete_otp_login(otp):
    global otp_pending, pass_pending
    try:
        await client.sign_in(phone, code=otp)
        otp_pending = False
        try:
            # check if 2FA needed
            await client.sign_in(password=None)
        except SessionPasswordNeededError:
            pass_pending = True
            print("🔒 2FA password required! Send /pass yourpassword")
        print("✅ Logged in via OTP")
    except Exception as e:
        print(f"❌ OTP login failed: {e}")

async def complete_password_login(password):
    global pass_pending
    try:
        await client.sign_in(password=password)
        pass_pending = False
        print("✅ 2FA login successful!")
    except Exception as e:
        print(f"❌ 2FA login failed: {e}")

# --- Start userbot ---
async def start_userbot():
    global otp_pending, pass_pending
    try:
        await client.start(phone=phone)  # Try existing session
        print("✅ Userbot running with existing session")
    except Exception:
        otp_pending = True
        print("⚠️ Session missing or expired! Send /otp <code> in your bot to login.")

    await client.run_until_disconnected()

# --- Run both ---
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    asyncio.run(start_userbot())
