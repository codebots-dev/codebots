import requests
import os

from codebots import TOKENS
from codebots.bots._bot import BaseBot

__all__ = [
    'TeleBot'
]

TELE_TOKEN = os.path .join(TOKENS, "telegram.json")


class TeleBot(BaseBot):
    """Bot that automatically sends messages over telegram

    Parameters
    ----------
    config_file : json
        json file containing the bot_token and the bot_chatID
    """

    def __init__(self, config_file=None) -> None:
        self.__name__ = "telebot"
        if not config_file:
            config_file = TELE_TOKEN
        super().__init__(config_file)
        self._credentials = self._get_token(config_file)
        self._url = self._compose_url()

    def _compose_url(self):
        """compose the base url to send the message

        Returns
        -------
        str
            base url
        """
        return 'https://api.telegram.org/bot' + self._credentials["bot_token"] + '/sendMessage?chat_id=' + self._credentials["bot_chatID"] + '&parse_mode=Markdown&text='

    def send_message(self, bot_message):
        """send the message over telegram

        Parameters
        ----------
        bot_message : str
            message to send

        Returns
        -------
        json
            response from the server
        """
        response = requests.get(self._url + bot_message)
        return response.json()


# if __name__ == '__main__':

#     # init the bot
#     bot = TeleBot('.tokens/telegram.json')

#     # send the message
#     bot.send_message('ciao mamma')
