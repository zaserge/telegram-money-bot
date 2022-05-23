# pylint: disable=C0111

from telebot import TeleBot
from telebot.types import Message, BotCommand


class BotSyntaxError(Exception):
    pass


class MoneyBot(TeleBot):

    text_messages = {
        'start':
            "Привет {name}.\n"
            "Это бот, который умеет конвертировать некоторые валюты",

        'help':
            "Бот знает следующие команды:\n"
            " /start Начало работы и эта справка\n"
            " /help Эта справка\n"
            " /list Список доступных валют\n"
            "Для того, чтобы сконвертировать валюту дайте команду боту в сдедующем формате:\n"
            "<исходная валюта> <требуемая валюта> <количество>\n"
            "Например: USD RUB 100"
    }

    def __init__(self, api_key: str, worker: object):
        TeleBot.__init__(self, api_key, num_threads=5)
        self.worker = worker
        self.register_message_handler(self.msg_start, commands=['start'], pass_bot=True)
        self.register_message_handler(self.msg_help, commands=['help'], pass_bot=True)
        self.register_message_handler(self.msg_list, commands=['list'], pass_bot=True)

        self.register_message_handler(self.msg_reply, content_types=["text"], pass_bot=True)

        self.set_my_commands([
            BotCommand("start", "Начало работы"),
            BotCommand("help", "Краткая справка"),
            BotCommand("list", "Список доступных валют")
        ])

    def start(self):
        self.polling()

    @ staticmethod
    def msg_start(message: Message, bot: TeleBot):
        bot.reply_to(message,
                     MoneyBot.text_messages['start'].format(name=message.from_user.first_name) +
                     "\n" + MoneyBot.text_messages['help'])

    @ staticmethod
    def msg_help(message: Message, bot: TeleBot):
        bot.reply_to(message, MoneyBot.text_messages['help'])

    @ staticmethod
    def msg_reply(message: Message, bot: TeleBot):
        try:
            if message.text.startswith("/"):
                raise BotSyntaxError(f"Неизвестная команда '{message.text}'")

            if len(message.text.split()) != 3:
                raise BotSyntaxError("Неправильное количество параметров")

            from_, to_, amount_ = message.text.upper().split()

            if from_ == to_:
                raise BotSyntaxError("Валюты одинаковые")

            res = bot.worker.exchange(from_, to_, amount_)
            answer = f"Стоимость {amount_} {from_} равна {res:.2f} {to_}"
        except Exception as err:  # pylint: disable=W0703
            answer = f"{type(err).__name__}: {str(err)}"

        bot.reply_to(message, answer)

    @ staticmethod
    def msg_list(message: Message, bot: TeleBot):
        answer = "Доступные валюты\n" + \
            "\n".join([f"  - {c} ({name})" for c, name in bot.worker.get_current_list().items()])
        bot.reply_to(message, answer)
