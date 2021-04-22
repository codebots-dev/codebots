from codebots.bots import DeployBot
from codebots.bots import sshBot

# set uo the bots
bot = DeployBot('/path/to/local/repo', '/path/to/server/repo', 'username@host')
sshbot = sshBot.from_credentials_file(".tokens/ssh.json")

# initial configuration (first time only)
bot.configure_local()
bot.configure_server(sshbot)

# deployment -> push the repo to the server
bot.deploy_to_server()
