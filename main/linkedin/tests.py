from django.test import TestCase
from linkedin.helpers import get_linkedin_post

# Create your tests here.
class LinkedinHelperFunctionTests(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_get_article_news_api(self):
        self.assertEqual(get_linkedin_post(), True)
