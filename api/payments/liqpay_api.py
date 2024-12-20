import os

import requests
from dotenv import load_dotenv
from liqpay.liqpay3 import LiqPay

load_dotenv()
PUBLIC_KEY = os.getenv("PUBLIC_KEY")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
liqpay = LiqPay(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)


def generate_url(order_id, amount: int, currency: str = "USD") -> str:
    params = {
        'action': 'pay',
        'amount': amount,
        'currency': currency,
        'description': 'Payment for clothes',
        'order_id': order_id,
        'version': '3',
        'sandbox': 1,
        'server_url': "https://locust-curious-dane.ngrok-free.app/pay/liqpay"
    }
    signature = liqpay.cnb_signature(params)
    data = liqpay.cnb_data(params)
    params = {"signature": signature, "data": data}
    response = requests.post("https://www.liqpay.ua/api/3/checkout/", params=params)
    print(response)
    return response.url


def get_order_status_from_liqpay(order_id: str) -> bool:
    res = liqpay.api("request", {
        "action": "status",
        "version": "3",
        "order_id": order_id
    })
    print(res)
    return res.get("type") == "buy" and res.get("result") == "ok"
