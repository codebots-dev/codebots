import os
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from codebots import SECRETS


__all__ = [
    'DriveBot'
]


class DriveBot():
    """Bot to help with handling your Google Drive.

    Parameters
    ----------
    authentication : str
        defines the authentication type. it can be either:
        - web : open the browser to sign in
        - local : uses previously stored credentials
        - path-to-credential-file: you can provide the full path to specific credentials
    save_credentials: bool, optional
        if True stores the credentials in the .tokens folder for future use.

    Attributes
    ----------
    authentication : str
        defines the authentication type. it can be either:
        - web : open the browser to sign in
        - local : uses previously stored credentials
        - path-to-credential-file: you can provide the full path to specific credentials
    save_credentials: bool, optional
        if True stores the credentials in the .tokens folder for future use, by default True.
    """

    def __init__(self, authentication, save_credentials=True) -> None:
        GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = SECRETS
        self._gauth = GoogleAuth()
        self._drive = self._authenticate(authentication, save_credentials)

    @property
    def gauth(self):
        """obj :  pydrive GoogleAuth object"""
        return self._gauth

    @property
    def drive(self):
        """obj :  pydrive GoogleDrive object"""
        return self._gdrive

    def _authenticate(self, authentication, save_credentials):
        """Sign in your Google Drive.

        Parameters
        ----------
        authentication : str
            defines the authentication type. it can be either:
            - web : open the browser to sign in
            - local : uses previously stored credentials
            - path-to-credential-file: you can provide the full path to specific credentials
        save_credentials: bool, optional
            if True stores the credentials in the .tokens folder for future use.

        Returns
        -------
        obj
            pydrive GoogleDrive object

        Raises
        ------
        FileNotFoundError
            You have to provide a valid (complete) path to the credential file or
            have previously saved it locally in the `.tokens` folder.
        """
        if authentication == 'web':
            self._authenticate_from_web(save_credentials)
        else:
            from .. import TOKENS
            if authentication == 'local':
                credentials = os.path.join(TOKENS, "drive.json")
                save_credentials = False
            else:
                credentials = authentication

            try:
                os.path.isfile(credentials)
            except Exception:
                raise FileNotFoundError('No credential file! You can generate one using drivebot from the command line')
            self._authenticate_from_file(credentials)

        return GoogleDrive(self._gauth)

    def _authenticate_from_web(self, save_credentials):
        """authenticate using a web interface.

        Parameters
        ----------
        save_credentials: bool, optional
            if True stores the credentials in the .tokens folder for future use.
        """
        # Create local webserver and auto handles authentication.
        self._gauth.LocalWebserverAuth()
        # Save the current credentials to a file
        if save_credentials:
            self._save_credentials()

    def _authenticate_from_file(self, credentials):
        """authenticate using a credential file

        Parameters
        ----------
        credentials : str
            complete path to the credential file
        """
        self._gauth.LoadCredentialsFile(credentials)

    def _save_credentials(self):
        """Save the authentication credential as a json file in the `.tokens`
        folder
        """
        from .. import TOKENS
        credentials = os.path.join(TOKENS, "drive.json")
        self._gauth.SaveCredentialsFile(credentials)

    def create_and_upload(self, name='Hello_World.txt', content='Hello World!'):
        """create a file with some content and upload it to your Google Drive.

        Parameters
        ----------
        path_to_file : str
            complete path to the file to upload.
        content : str
            content of the file.
        """
        file1 = self._drive.CreateFile({'title': name})  # Create GoogleDriveFile instance with title 'Hello.txt'.
        file1.SetContentString(content)  # Set content of the file from given string.
        file1.Upload()

    def upload_local_file(self, path_to_file, name):
        """upload a file to your Google Drive.

        Parameters
        ----------
        path_to_file : str
            complete path to the file to upload.
        """
        file1 = self._drive.CreateFile()
        file1.SetContentFile(path_to_file)
        file1['title'] = name
        file1.Upload()
        print('File successfully uploaded!')


if __name__ == '__main__':
    pass
