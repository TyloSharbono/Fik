import re, asyncio, threading
from telethon import TelegramClient, events
import telebot

# --- Hardcoded User API (Real User) ---
api_id = 20141517
api_hash = "40705a00a70d2a57757b9c24e6e297af"
phone = "+918538929537"
client = TelegramClient("session", api_id, api_hash)

# --- Hardcoded Bot API (Featured Bot) ---
BOT_TOKEN = "8384695302:AAHUfY9Q8iL2j_4nRnTivsl2C8SgKl6W74Q"
bot = telebot.TeleBot(BOT_TOKEN)

# --- Settings ---
ADMIN_ID = 8009385011
TARGET_CHANNEL = -1002089891838
keywords = ["approved", "charge", "valid", "thank you", "card added", "successful", "added"]
bot_active = False

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

# --- Run both together ---
def run_bot():
    bot.infinity_polling()

async def run_userbot():
    await client.start()  # Uses session.session
    print("Userbot running...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    asyncio.run(run_userbot())
