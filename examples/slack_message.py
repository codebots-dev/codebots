from codebots.slackbot import SlackBot

# Create a bot: you need to specify the location of the access token file ".tokens/slack"
bot = SlackBot(".tokens/slack")

# Ask the bot to send a test message to a the 'general' channel of your workspace
bot.send_message(channel='general', message='test')
