from codebots.bots import DeployBot

# set uo the bots
bot = DeployBot('my_project')

# deployment -> push the repo to the server
bot.deploy_to_server(local_name="main")
