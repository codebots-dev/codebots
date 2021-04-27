from codebots.bots import SlackBot

# Create a SlackBot instance from the credentials that you have set-up before
# (if you don't know how, check the documentation page)
bot = SlackBot()

# or create a bot an access token file ".tokens/slack.json"
# bot = SlackBot(".tokens/slack.json")

# Ask the bot to send a test message to a the 'general' channel of your workspace
bot.send_message(channel='general', message='test')
