from googleapiclient.discovery import build
from oauth2client.client import AccessTokenCredentials
import httplib2
from authentication.helpers import check_google_token


class BloggerHelper(object):
    def __init__(self) -> None:
        self.access_token = check_google_token()

        # Set up credentials
        credentials = AccessTokenCredentials(self.access_token, "my-user-agent/1.0")
        http = httplib2.Http()
        http = credentials.authorize(http)

        self.service = build("blogger", "v3", http=http)
        self.blog_id = "1793487694780974605"

    def create_posts(self, title, content):
        # Create a new blog post
        body = {"title": "Test", "content": "Test"}

        try:
            posts = self.service.posts()
            request = posts.list(blogId=self.blog_id)
            response = posts.insert(blogId=self.blog_id, body=body).execute()
            print("Post created. Post ID: %s" % response["id"])
        except Exception as e:
            print(e)
