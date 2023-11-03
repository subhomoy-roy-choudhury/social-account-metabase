from mega import Mega
from django.conf import settings

mega = Mega()

class MegaFileUploader(object):
    def __init__(self) -> None:
        self.mega = mega.login(settings.MEGA_USERNAME, settings.MEGA_PASSWORD)

    def upload_file(self, filepath, destination_file_path):
        folder_destination = self.mega.find(destination_file_path)
        file = self.mega.upload(filepath, folder_destination[0])
        return self.mega.get_upload_link(file)