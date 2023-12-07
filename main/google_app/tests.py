from django.test import TestCase
from google_app.helpers import BloggerHelper


# Create your tests here.
class BloggerHelpersFunctionTests(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.blogger_client = BloggerHelper()

    def test_create_blogger_post(self):
        self.assertEqual(
            self.blogger_client.create_posts("I have the answer", "Eureka! It is 42!"),
            True,
        )
