import logging

import aiohttp

TON_API_URL = "https://tonapi.io/v2/"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 0:d56cc486e5000fc567cf1dea9f3f66cdf55be313240ff66f1755bcc6729d70a4

async def check_payment(wallet_address: str, memo: str, required_amount: float) -> tuple[bool, bool]:
    try:
        async with aiohttp.ClientSession() as session:
            url = f"{TON_API_URL}blockchain/accounts/{wallet_address}/transactions?limit=100"
            async with session.get(url) as response:
                data = await response.json()
                if response.status != 200 or data.get("error"):
                    logger.error(f"Ошибка запроса к TON API: {response.status}")
                    return False, True
                logger.info("OK")
                for i, tx in enumerate(data.get("transactions", [])):
                    out_msgs = tx.get('out_msgs')
                    in_msg = tx.get('in_msg')
                    if out_msgs:
                        transaction_value_grams = tx['out_msgs'][0]['value']
                        print(f'value: {transaction_value_grams}')
                        transaction_value_ton = transaction_value_grams / 1_000_000_000
                        print(f'transactions ton: {transaction_value_grams}')
                        message = str(tx['out_msgs'][0])
                        print(f"MESS: {message}")
                        has = memo in message
                        print(f"out HAS: {has}")
                        if has and transaction_value_ton >= required_amount:
                            return True, False
                    if in_msg:
                        transaction_value_grams = tx['in_msg']['value']
                        print(f'in value: {transaction_value_grams}')
                        transaction_value_ton = transaction_value_grams / 1_000_000_000
                        print(f'in transactions ton: {transaction_value_grams}')
                        message = str(tx['in_msg'])
                        print(f"in MESS: {message}")
                        has = memo in message
                        print(f"in HAS: {has}")
                        if has and transaction_value_ton >= required_amount:
                            return True, False
        return False, False
    except Exception as e:
        logger.error(f"Error: module 'ton.py', method: 'check_payment', reason: {e}")
        return False, True
