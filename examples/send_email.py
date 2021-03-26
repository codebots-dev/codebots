from bots import EmailBot
from bots import Sender

# initiate the Sender with some credentials:
# - you can specify the location of the access config file ".tokens/email" (keep this secret!)
# - or you can pass username and password on the fly (not a great idea...)
sender = Sender.form_file(".tokens/email")

# Crete the bot: not it can send emails on behalf of the Sender account
bot = EmailBot(sender)

# set the email content
receiver = "francesco.ranaudo@gmail.com"
subject = "message from bot"
body = "This message was sent by a bot"

# Ask the bot to compose your email and send it
bot.send_email(receiver, subject, body)
