import json
import requests
from config import keys

class APIException(Exception):
    pass

class CurConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        quote = quote.lower()
        base = base.lower()
        if quote == base:
            raise APIException(f'Введите разные валюты')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}. Проверьте орфографию!')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}. Может, опечатка?')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}. Введите число!')


        quote_ticker, base_ticker = keys[quote].lower(), keys[base].lower()
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * amount

        return total_base

