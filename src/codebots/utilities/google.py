import os
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from codebots import SECRETS

GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = SECRETS

# import os
# print(os.getcwd())

gauth = GoogleAuth()
# Create local webserver and auto handles authentication.
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

file1 = drive.CreateFile({'title': 'Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
file1.SetContentString('Hello World!')  # Set content of the file from given string.
file1.Upload()

# if __name__ == "__main__":
#     pass


# For using listdir()


# # Below code does the authentication
# # part of the code
# gauth = GoogleAuth()

# # Creates local webserver and auto
# # handles authentication.
# gauth.LocalWebserverAuth()
# drive = GoogleDrive(gauth)

# # replace the value of this variable
# # with the absolute path of the directory
# path = r"C:\Games\Battlefield"

# # iterating thought all the files/folder
# # of the desired directory
# for x in os.listdir(path):

#     f = drive.CreateFile({'title': x})
#     f.SetContentFile(os.path.join(path, x))
#     f.Upload()

#     # Due to a known bug in pydrive if we
#     # don't empty the variable used to
#     # upload the files to Google Drive the
#     # file stays open in memory and causes a
#     # memory leak, therefore preventing its
#     # deletion
#     f = None
