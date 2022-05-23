# pylint: disable=C0111

import config
import currency_exchange as ce
import money_bot as mbot


def main():
    exchange_worker = ce.CurrencyExchange(config.CURRENCY_DATA_API)
    bot = mbot.MoneyBot(config.TELEGRAM_BOT_API_KEY, exchange_worker)
    bot.start()


if __name__ == '__main__':
    main()
