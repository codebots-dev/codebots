# send email over gmail

import yagmail

__all__=[
    'Sender',
    'EmailBot'
]

class Sender():
    def __init__(self, **kwargs) -> None:
        self._username = kwargs.get('username', None)
        self._password = kwargs.get('password', None)

    @property
    def username(self):
        return self._username

    @property
    def password(self):
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
    def __init__(self, sender) -> None:
        self.sender = sender

    def send_email(self, receiver,subject, body, attachment=None):

        yag = yagmail.SMTP(self.sender.username, self.sender.password)
        yag.send(
            to=receiver,
            subject=subject,
            contents=body,
            attachments=attachment,
        )

# Debug
if __name__ == "__main__":
    sender = Sender.form_file("config")
    receiver = "francesco.ranaudo@gmail.com"
    subject = "message from bot"
    body = "This message was sent by a bot"
    filename = "document.pdf"

    bot = EmailBot(sender)
    bot.send_email(receiver, subject, body)

