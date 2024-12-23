import requests


def get_uan_price():
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'usd',  # USD используется как базовый идентификатор
        'vs_currencies': 'uah'  # Запрашиваем цену USD в UAH
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print(data)  # Для отладки
        if 'usd' in data:
            return data['usd']['uah']
        else:
            print("Ключ 'usd' отсутствует в ответе")
            return None
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при получении данных: {e}')
        return None


def get_require(amount_usd: int = 4) -> int:
    try:
        uan_price = get_uan_price()
        return round(uan_price * amount_usd)
    except Exception as e:
        print(f"ERROR/ currency.py / method get_require: {e}")
        return 165
