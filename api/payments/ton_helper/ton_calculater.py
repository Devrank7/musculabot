import requests


def get_ton_price():
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'the-open-network',
        'vs_currencies': 'usd'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'the-open-network' in data:
            return data['the-open-network']['usd']
        else:
            print("Ключ 'the-open-network' отсутствует в ответе")
            return None
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при получении данных: {e}')
        return None


def calculate_ton_for_amount(ton_price_usd, amount_usd):
    """
    Рассчитывает, сколько TON нужно для оплаты заданной суммы в USD.

    :param ton_price_usd: Цена одного TON в долларах.
    :param amount_usd: Сумма в долларах, которую нужно оплатить.
    :return: Количество TON, необходимое для оплаты.
    """
    try:
        if ton_price_usd <= 0:
            raise ValueError("Цена TON должна быть больше нуля.")
        return round((amount_usd / ton_price_usd), 5)
    except Exception as e:
        print(f"Ошибка при расчете: {e}")
        return None


def get_require_ton(amount_usd: int = 4):
    ton_price = get_ton_price()
    return calculate_ton_for_amount(ton_price, amount_usd)
