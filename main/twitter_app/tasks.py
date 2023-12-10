from celery import shared_task
from django.utils import timezone
from authentication.helpers import check_twitter_token

from twitter_app.helpers import create_tweets, get_research_paper_tweet_content
from twitter_app.models import Tweet

@shared_task(name="daily_arvix_research_paper_tweets")
def daily_arvix_research_paper_tweets():
        # Get today's date
    today = timezone.now().date()

    # check Linkedin access token
    try:
        access_token, error = check_twitter_token()
        if access_token:
            # Try to get the LinkedinPost for today
            daily_tweets_count = Tweet.objects.filter(
                created_at__date=today
            ).count()
            if daily_tweets_count > 0:
                print(f"Tweet Already created on {today.strftime('%B %d, %Y')}")
            else:
                tweet_content = get_research_paper_tweet_content()
                # Create Tweet
                tweet_id, tweet_content = create_tweets(access_token, tweet_content)
                Tweet.objects.create(
                    created_at=today,
                    markdown=tweet_content,
                    tweet_id=tweet_id,
                    is_send=True,
                )
                print("Tweet Created Successfully!")
        else:
            print(error)
    except Exception as e:
        raise Exception(e)