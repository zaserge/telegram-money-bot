# pylint: disable=C0111

from telebot import TeleBot
from telebot.types import Message, BotCommand

text_messages = {
    'welcome':
        'Please welcome {name}!\n\n'
        'This chat is intended for questions about and discussion of the pyTelegramBotAPI.\n'
        'To enable group members to answer your questions fast and accurately, '
        'please make sure to study the '
        'I hope you enjoy your stay here!',

    'info':
        'My name is TeleBot,\n'
        'I am a bot that assists these wonderful bot-creating people of this bot '
        'library group chat.\n'
        'Suggestions are also welcome, just drop them in this group chat!',

    'wrong_chat':
        'Hi there!\nThanks for trying me out. However, this '
        'bot can only be used in the pyTelegramAPI group chat.\n'
        'Join us!\n\n'
        'https://telegram.me/joinchat/067e22c60035523fda8f6025ee87e30b'
}


class MoneyBot(TeleBot):

    def __init__(self, api_key: str, worker: object):
        TeleBot.__init__(self, api_key, num_threads=5)
        self.worker = worker
        self.register_message_handler(self.msg_start, commands=['start'], pass_bot=True)
        self.register_message_handler(self.msg_help, commands=['help'], pass_bot=True)
        self.register_message_handler(self.msg_list, commands=['list'], pass_bot=True)
        self.register_message_handler(self.msg_exchange, commands=['exchange'], pass_bot=True)

        self.register_message_handler(self.msg_reply, content_types=["text"], pass_bot=True)

        self.set_my_commands([
            BotCommand("start", "main menu"),
            BotCommand("help", "print usage"),
            BotCommand("list", "available currency list"),
            BotCommand("exchange", "currency exchange")
        ])

    def start(self):
        self.polling()

    @ staticmethod
    def msg_start(message: Message, bot: TeleBot):
        bot.reply_to(message, "This is greeting message")

    @ staticmethod
    def msg_help(message: Message, bot: TeleBot):
        bot.reply_to(message, "/start\n/restart\n/list\n/exchange")

    @ staticmethod
    def msg_reply(message: Message, bot: TeleBot):
        if message.text.startswith("/"):
            bot.reply_to(message, f"unknown command ({message.text})")
        else:
            bot.reply_to(message,
                         "conversations not implemented yet")

    @ staticmethod
    def msg_exchange(message: Message, bot: TeleBot):
        try:
            answer = bot.worker.exchange("USD1", "RUB", "1000")
        except Exception as err:  # pylint: disable=W0703
            answer = str(err)
        bot.reply_to(message, answer)

    @ staticmethod
    def msg_list(message: Message, bot: TeleBot):
        bot.reply_to(message, "\n".join(
            [f"- {c} ({name})" for c, name in bot.worker.get_current_list().items()]))
