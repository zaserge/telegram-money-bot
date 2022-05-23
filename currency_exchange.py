# pylint: disable=C0111

import requests


class ExchangeAPIException(Exception):
    pass


class CurrencyExchange(object):

    CONVERT_URL = 'https://api.apilayer.com/exchangerates_data/convert'
    CURRENCY_LIST = {
        'RUB': 'Рубли',
        'USD': 'US dollar',
        'EUR': 'Euro'
    }

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_current_list(self):
        return CurrencyExchange.CURRENCY_LIST

    def exchange(self, source: str, dest: str, value: float):

        if source not in CurrencyExchange.CURRENCY_LIST:
            raise ExchangeAPIException(f"Неизвестная валюта ({source})")

        if dest not in CurrencyExchange.CURRENCY_LIST:
            raise ExchangeAPIException(f"Неизвестная валюта ({dest})")

        try:
            amount = float(value)
        except ValueError:
            amount = None

        if not amount:
            raise ValueError(f"Количество ошибочное ({value})")

        if amount <= 0:
            raise ValueError(f"Количество не может быть отрицательным ({value})")

        headers = {'apikey': self.api_key}
        params = {
            'from':     source,
            'to':       dest,
            'amount':   amount
        }

        response = requests.get(CurrencyExchange.CONVERT_URL, params=params, headers=headers).json()

        # response = {'success': True,
        #             'query': {'from': 'RUB', 'to': 'EUR', 'amount': 25.5},
        #             'info': {'timestamp': 1653254403, 'rate': 0.015269},
        #             'date': '2022-05-22',
        #             'result': 389.3623}

        if response and response.get('result'):
            return round(response.get('result'), 2)

        raise ExchangeAPIException(f"Ошибка сервера. {response['message']}")

    @staticmethod
    def get_price(base: str, quote: str, amount: float, apikey: str):
        ex = CurrencyExchange(apikey)
        return ex.exchange(base, quote, amount)
