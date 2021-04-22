import yagmail

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
            username = f.readline()
            password = f.readline()
        user = cls(username=username, password=password)
        return user


class EmailBot:
    """EmailBot.

    Parameters
    ----------
    sender : obj
        Sender object configured with sender account credentials.
    """

    def __init__(self, sender) -> None:
        self.sender = sender

    def send_email(self, receiver, subject, body, attachment=None):
        """Send an email to an email address.

        Parameters
        ----------
        receiver : str
            email address of the receiver
        subject : str
            subject of the email
        body : [type]
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


# # Debug
# if __name__ == "__main__":
#     sender = Sender.form_file(".tokens/email")
#     receiver = "francesco.ranaudo@gmail.com"
#     subject = "message from bot"
#     body = "This message was sent by a bot"
#     filename = "document.pdf"

#     bot = EmailBot(sender)
#     bot.send_email(receiver, subject, body)
