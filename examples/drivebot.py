from codebots.bots import DriveBot

# create a DriveBot using a web authentication and store the credentials
dbot = DriveBot('web', True)

dbot.create_and_upload(name='my_first_upload.txt',
                       content='codebots is awesome!')
