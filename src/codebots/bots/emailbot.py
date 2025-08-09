import yagmail
import json
import os

from ._bot import BaseBot

__all__ = [
    'Sender',
    'EmailBot'
]


class Sender():
    """Sender class to manage the sender email settings.

    Parameters
    ----------
    username : str
        username used to access the sender email account
    password : str
        password used to access the seder email account
    """

    def __init__(self, username=None, password=None, config_file=None):
        # Modern token handling: env vars first, then config file
        if username and password:
            self._username = username
            self._password = password
        else:
            env_user = os.getenv("EMAILBOT_USERNAME")
            env_pass = os.getenv("EMAILBOT_PASSWORD")
            if env_user and env_pass:
                self._username = env_user
                self._password = env_pass
            elif config_file:
                with open(config_file, "r") as f:
                    credentials = json.load(f)
                self._username = credentials["username"]
                self._password = credentials["password"]
            else:
                raise ValueError("Email credentials not found. Set EMAILBOT_USERNAME and EMAILBOT_PASSWORD env vars or provide a config file.")

    @property
    def username(self):
        """str : username used to access the sender email account"""
        return self._username

    @property
    def password(self):
        """str : password used to access the sender email account"""
        return self._password

    @classmethod
    def from_file(cls, config_file):
        """read the access token form a file.

        Returns
        -------
        str
            access token
        """
        with open(config_file, "r") as f:
            credentials = json.load(f)
        return cls(username=credentials["username"], password=credentials["password"])


class EmailBot(BaseBot):
    """EmailBot.

    Parameters
    ----------
    sender : obj
        Sender object configured with sender account credentials.
    """

    def __init__(self, config_file=None, sender=None) -> None:
        if not sender:
            if not config_file:
                from .. import TOKENS
                config_file = os.path.join(TOKENS, "email.json")
            super().__init__(config_file)
            # Ensure sender is set from credentials
            self.sender = Sender(self._credentials.get("username"), self._credentials.get("password"))
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
