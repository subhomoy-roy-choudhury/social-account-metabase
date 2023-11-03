from django.conf import settings

# key = getpass(settings.STORJ_ACCESS_KEY)
# secret = getpass(settings.STORJ_SECRET_KEY)
# storage_options={"key":key, "secret":secret, "client_kwargs": {'endpoint_url':"https://gateway.storjshare.io"}}

# Create a connection to Storj
# storjS3 = s3fs.S3FileSystem(anon=False, key=settings.STORJ_ACCESS_KEY, secret=settings.STORJ_SECRET_KEY, endpoint_url="https://gateway.storjshare.io")

class StorjFileUploader(object):
    def __init__(self) -> None:
        self.storj_client = None

    def upload_file(self, filepath, destination_file_path):
        raise Exception("Not Implemented")