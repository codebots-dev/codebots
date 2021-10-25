import authentication
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os


from ._bot import BaseBot

__all__ = [
    'DriveBot'
]


class DriveBot(BaseBot):
    """Bot to help with handling your Google Drive.


    """

    def __init__(self, config_file) -> None:
        super().__init__(config_file)


def docxDriveUpload(service):

    file_metadata = {'name': 'otuput.docx'}
    media = MediaFileUpload(
        'output.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print('File upload successful! File ID: %s' % file.get('id'))


if __name__ == '__main__':
    docxDriveUpload()
