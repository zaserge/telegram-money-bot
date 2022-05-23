# pylint: disable=C0111

import json
import requests


class APIException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class CurrencyExchange(object):

    CONVERT_URL = 'https://api.apilayer.com/exchangerates_data/convert'
    CURRENCY_LIST = {
        'RUB': 'Ruble',
        'USD': 'US dollar',
        'EUR': 'Euro'
    }

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_current_list(self):
        return CurrencyExchange.CURRENCY_LIST

    def exchange(self, source: str, dest: str, value: float):

        if source not in CurrencyExchange.CURRENCY_LIST:
            raise APIException(f"Currency is unknown ({source})")

        if dest not in CurrencyExchange.CURRENCY_LIST:
            raise APIException(f"Currency is unknown ({dest})")

        try:
            amount = float(value)
        except ValueError:
            amount = None

        if not amount:
            raise APIException(f"Currency amount is incorrect ({value})")

        if amount <= 0:
            raise APIException(f"Currency amount is negative ({value})")

        headers = {'apikey': self.api_key}
        params = {
            'from':     source,
            'to':       dest,
            'amount':   amount
        }

        #r = requests.get(CurrencyExchange.CONVERT_URL, params=params, headers=headers)
        #response = r.json()
        response = {'success': True,
                    'query': {'from': 'RUB', 'to': 'EUR', 'amount': 25.5},
                    'info': {'timestamp': 1653254403, 'rate': 0.015269},
                    'date': '2022-05-22',
                    'result': 389.3623}

        if response and response.get('result'):
            # return f"{amount:.2f} {source} = {round(response.get('result'), 2):.2f} {dest}"
            return round(response.get('result'), 2)
        else:
            raise APIException("Unknown server error")

    @staticmethod
    def get_price(base: str, quote: str, amount: float, apikey: str):
        ex = CurrencyExchange(apikey)
        return ex.exchange(base, quote, amount)
