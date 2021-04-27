import yagmail
import json
import os
from codebots import TOKENS
from codebots.bots._bot import BaseBot

__all__ = [
    'Sender',
    'EmailBot'
]

EMAIL_TOKEN = os.path.join(TOKENS, "email.json")


class Sender():
    """Sender class to manage the sender email settings.

    Parameters
    ----------
    username : str
        username used to access the sender email account
    password : str
        password used to access the seder email account
    """

    def __init__(self, username, password) -> None:
        self._username = username
        self._password = password

    @property
    def username(self):
        """str : username used to access the sender email account"""
        return self._username

    @property
    def password(self):
        """str : password used to access the sender email account"""
        return self._password

    @classmethod
    def form_file(cls, config_file):
        """read the access token form a file.

        Returns
        -------
        str
            access token
        """

        with open(config_file, "r") as f:
            credentials = json.load(f)
        user = cls(username=credentials["username"], password=credentials["password"])
        return user


class EmailBot(BaseBot):
    """EmailBot.

    Parameters
    ----------
    sender : obj
        Sender object configured with sender account credentials.
    """

    def __init__(self, config_file=None, sender=None) -> None:

        self.__name__ = "emailbot"
        if not sender:
            if not config_file:
                config_file = EMAIL_TOKEN
            super().__init__(config_file)
            self._credentials = self._get_token(config_file)
            self.sender = Sender(self._credentials["username"], self._credentials["password"])
        else:
            if not isinstance(sender, Sender):
                raise ValueError("the sender is not valid")
            self.sender = sender

    def send_email(self, receiver, subject, body, attachment=None):
        """Send an email to an email address.

        Parameters
        ----------
        receiver : str
            email address of the receiver
        subject : str
            subject of the email
        body : str
            body text of the email
        attachment : str, optional
            path to the file to attach, by default None
        """
        yag = yagmail.SMTP(self.sender.username, self.sender.password)
        yag.send(
            to=receiver,
            subject=subject,
            contents=body,
            attachments=attachment,
        )


        # Debug
if __name__ == "__main__":
    # sender = Sender.form_file("C:/Users/franaudo/.tokens/email.json")
    receiver = "francesco.ranaudo@gmail.com"
    subject = "message from bot"
    body = "This message was sent by a bot"
    filename = "document.pdf"

    # bot = EmailBot(sender)
    bot = EmailBot()
    bot.send_email(receiver, subject, body)
