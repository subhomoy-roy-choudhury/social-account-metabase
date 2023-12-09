from django.test import TestCase
from twitter_app.tasks import daily_arvix_research_paper_tweets
from twitter_app.helpers import get_research_paper_tweet_content

# Create your tests here.
class TwitterTasksFunctionTests(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_get_article_news_api(self):
        self.assertEqual(get_research_paper_tweet_content(), True)