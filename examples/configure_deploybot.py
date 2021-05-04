from codebots.bots import DeployBot
from codebots.utilities.deploy import configure_server

project = 'my_project'
address = "username@host"
local = "C:/test"
server = "/home/username/test_deploybot"

bot = DeployBot(project)
out = configure_server(bot.server_repo_path)

print(out)
