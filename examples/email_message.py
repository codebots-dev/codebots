from codebots.bots import EmailBot

# Crete the bot: not it can send emails on behalf of the Sender account
bot = EmailBot()

# # If you want send an email from another account, initiate a Sender
# # with some credentials and feed it to the emailbot:
# # - you can specify the location of the access config file ".tokens/email" (keep this secret!)
# # - or you can pass username and password on the fly (not a great idea...)
# from codebots.bots import Sender
# sender = Sender.form_file(".tokens/email")
# bot = EmailBot(sender)

# set the email content
receiver = "receiver@email.com"
subject = "message from bot"
body = "This message was sent by a bot"

# Ask the bot to compose your email and send it
bot.send_email(receiver, subject, body)
