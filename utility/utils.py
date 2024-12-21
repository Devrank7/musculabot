import hashlib
import hmac
import random
import string
from datetime import datetime

from db.sql.model import User


def check_access_for_chanel(user: User) -> bool:
    if user.date_of_kill is None:
        return False
    return user.date_of_kill > datetime.now()


def generate_random_code():
    return ''.join(random.choices(string.ascii_letters, k=10))


def generate_hmac_md5(merchant_account, merchant_domain_name, order_reference, order_date, amounts, currency,
                      product_names, product_counts, product_prices, secret_key):
    if not (len(product_names) == len(product_counts) == len(product_prices)):
        raise ValueError("Списки product_names, product_counts і product_prices повинні бути однакової довжини")
    data_list = [
        merchant_account,
        merchant_domain_name,
        order_reference,
        order_date,
        str(amounts),
        currency
    ]
    data_list += product_names
    data_list += product_counts
    data_list += product_prices
    data_string = ';'.join([str(i) for i in data_list])
    print(data_string)
    hmac_md5 = hmac.new(secret_key.encode('utf-8'), data_string.encode('utf-8'), hashlib.md5).hexdigest()
    return hmac_md5
