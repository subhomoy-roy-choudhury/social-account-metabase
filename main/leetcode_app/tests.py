from django.test import TestCase
from leetcode_app.helpers import get_all_leetcode_questions
from leetcode_app.tasks import solved_leetcode_question_scraper

# Create your tests here.
class LeetcodeHelperFunctionTests(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    def test_get_leetcode_questions(self):
        self.assertListEqual(get_all_leetcode_questions(), True)

class LeetcodeTaskFunctionTests(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    def test_soved_leetcode_question_scraper(self):
        self.assertEqual(solved_leetcode_question_scraper(), True)
