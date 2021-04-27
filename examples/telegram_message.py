from codebots.bots import TeleBot

# Create a TeleBot instance from the credentials that you have set-up before
# (if you don't know how, check the documentation page)
bot = TeleBot()

# # or create a bot an access token file ".tokens/telegram.json"
# bot = TeleBot('.tokens/telegram.json')

# Ask the bot to send a test message
bot.send_message('ciao mamma')
