import logging
import os
from typing import Any

from dotenv import load_dotenv
from pycoinpayments import CoinPayments

load_dotenv()
COINPAYMENTS_PUBLIC_KEY = os.getenv("COINPAYMENTS_PUBLIC_KEY")
COINPAYMENTS_PRIVATE_KEY = os.getenv("COINPAYMENTS_PRIVATE_KEY")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cp_client = CoinPayments(public_key=COINPAYMENTS_PUBLIC_KEY, private_key=COINPAYMENTS_PRIVATE_KEY)


def create_transaction(amount: int, name: str, email: str, currency1: str = "USDT.TRC20", currency2: str = "USDT.TRC20") \
        -> tuple[str, str]:
    try:
        create_transaction_params = {
            'amount': amount,
            'currency1': currency1,
            'currency2': currency2,
            'buyer_email': email,  # Email покупателя
            'item_name': name
        }
        info = cp_client.get_basic_info()
        print(f'info = {info}')
        payment = cp_client.create_transaction(create_transaction_params)
        logger.info(f"Payment: {payment}")
        return payment['txn_id'], payment['checkout_url']
    except Exception as e:
        logger.error(f"Error in 'coinpayments.py', method: 'create_transaction', reason: {e} ")


def check_payment_status(txn_id) -> [Any, bool]:
    try:
        status = cp_client.get_tx_info({"txid": txn_id})
        logger.info(f"Status: {status}")
        return status, int(status['status']) == 1
    except Exception as e:
        logger.error(f"Error n 'coinpayments.py', method: 'check_payment_status', reason: {e} ")
