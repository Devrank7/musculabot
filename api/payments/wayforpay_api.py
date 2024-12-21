import logging
import os
import time

import httpx
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from utility.utils import generate_hmac_md5

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()
MERCHANT_ACCOUNT = os.getenv("MERCHANT_ACCOUNT")
MERCHANT_SECRET_KEY = os.getenv('WFP_SECRET_KEY')
MERCHANT_PASSWORD = os.getenv("MERCHANT_PASSWORD")


def create_regular_invoice(order_id):
    try:
        data = {
            "merchantAccount": MERCHANT_ACCOUNT,
            "merchantAuthType": "SimpleSignature",
            "merchantDomainName": "mikeboreyko_com",
            "orderReference": order_id,
            "orderDate": str(int(time.time())),
            "amount": "165",
            "currency": "UAH",
            "orderTimeout": "49000",
            "productName[]": ["Подписка на телеграм канал"],
            "productPrice[]": ["165"],
            "productCount[]": ["1"],
            "merchantSignature": "487d4fd48ca0b4a38a85e6cfd0c0c9f8",
            'regularMode': 'monthly',
            'regularOn': '1',
            'regularCount': '12',
            'language': 'RU'
        }
        data['merchantSignature'] = generate_hmac_md5(
            data['merchantAccount'],
            data['merchantDomainName'],
            data['orderReference'],
            data['orderDate'],
            data['amount'],
            data['currency'],
            data['productName[]'],
            data['productCount[]'],
            data['productPrice[]'],
            MERCHANT_SECRET_KEY)

        rest = requests.post(
            'https://secure.wayforpay.com/pay',
            data=data
        )
        print(f"Rest: {rest.text}")
        return 'https://secure.wayforpay.com' + BeautifulSoup(rest.text, features="html.parser").find('form', id='cardpay')['action'], data[
            'merchantSignature']
    except Exception as e:
        logger.error(f"Error: module 'wayforpay_api.py', method 'create_regular_invoice', reason: {e}")


async def check_regular_invoice(order_id):
    try:
        response = await httpx.AsyncClient().post('https://api.wayforpay.com/regularApi', json={
            "requestType": "STATUS",
            "merchantAccount": MERCHANT_ACCOUNT,
            "merchantPassword": MERCHANT_PASSWORD,
            'orderReference': order_id
        }, timeout=20.0)
        print(response.json())
        return response.json()
    except Exception as e:
        logger.error(f"Error: module 'wayforpay_api.py', method 'check_regular_invoice', reason: {e}")


async def check_ok_regular_invoice(order_id):
    try:
        json = await check_regular_invoice(order_id)
        if json is None:
            logger.info("Json is NONE")
            return False
        return json['status'] == 'Active'
    except Exception as e:
        logger.error(f"Error: module 'wayforpay_api.py', method 'check_ok_regular_invoice', reason: {e}")


async def remove_regular_invoice(order_id):
    try:
        url = 'https://api.wayforpay.com/regularApi'
        a = await httpx.AsyncClient().post(url, json={
            "requestType": "REMOVE",
            "merchantAccount": MERCHANT_ACCOUNT,
            "merchantPassword": MERCHANT_PASSWORD,
            'orderReference': order_id
        })
        print(a.json())
        return a.json()
    except Exception as e:
        logger.error(f"Error: module 'wayforpay_api.py', method 'remove_regular_invoice', reason: {e}")
