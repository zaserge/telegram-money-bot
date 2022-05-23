# Money Exchange Rate Bot

- Бот возвращает цену на определённое количество валюты (евро, доллар или рубль).
- Использует библиотеку pyTelegramBotAPI.
- Формат запроса `<from> <to> <amount>`
- **/start** и **/help** выводят краткую инструкцию.
- **/list** выводит список доступных валют.
- используется API <https://api.apilayer.com/exchangerates_data>
- При ошибке пользователя вызывается исключение с текстом пояснения ошибки.
- Текст любой ошибки с указанием типа ошибки отправляется пользователю в сообщения.
- Создан `class CurrencyExchange` со статическим методом `get_price()`, который принимает ~~три~~ четыре аргумента: имя валюты, цену на которую надо узнать, — `base`, имя валюты, цену в которой надо узнать, — `quote`, количество переводимой валюты — `amount` и возвращает нужную сумму в валюте. Четвертый это `API_KEY`. Без него можно, но тогда его надо поместить внутри кода класса, что, по моему, не совсем правильно.
- Токен telegramm-бота хранится в `config.py`
- Токен exchange-api хранится в `config.py`
- `class CurrencyExchange` в *currency_exchange.py*
  - `exchange(self, source: str, dest: str, value: float)`
  - статичный метод `get_price(base: str, quote: str, amount: float, apikey: str)`

- `class MoneyBot` в *money_bot.py*
  - `__init__(self, api_key: str, worker: object)`
  - `start()`
  