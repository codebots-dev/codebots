from codebots import TeleBot

# Create a bot: you need to specify the location of the access token file ".tokens/telegram.json"
bot = TeleBot('.tokens/telegram.json')

# Ask the bot to send a test message
bot.send_message('ciao mamma')
