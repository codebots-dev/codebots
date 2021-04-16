from codebots.bots import sshBot

# execute command on the server
bot = sshBot.from_credentials_file(".tokens/home.json")
bot.exectute_cmds(commands=['ls'])  # note: the imput is a list!

# get folder content
remotefolderpath = '/home/server/Documents/test/'
localfolderpath = '/home/client/Documents/'
bot.get_folder_from_server(remotefolderpath, localfolderpath)
