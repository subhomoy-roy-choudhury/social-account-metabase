from django.test import TestCase
from github_app.helpers import GithubHelper

# Create your tests here.
class GithubHelperFunctionTests(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.github_helper = GithubHelper()

    def test_girhub_add_file(self):
        self.assertEqual(self.github_helper.add_file(), True)