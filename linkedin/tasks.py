from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from linkedin.models import LinkedinPost
from linkedin.helpers import get_linkedin_post
from authentication.helpers import check_linkedin_token


@shared_task(name="daily_linkedin_post")
def daily_linkedin_post():
    # Get today's date
    today = timezone.now().date()

    # check Linkedin access token
    check_token, error = check_linkedin_token()
    if check_token:
        try:
            # Try to get the LinkedinPost for today
            daily_linkedin_post = LinkedinPost.objects.get(created_at__date=today)
            print(f"Linkedin Post Already created on {today.strftime('%B %d, %Y')}")

        except ObjectDoesNotExist:
            # If post doesn't exist, then fetch the LinkedIn post and create the object
            markdown_content = get_linkedin_post()
            daily_linkedin_post = LinkedinPost.objects.create(
                created_at=today, markdown=markdown_content
            )
            print("Linkedin Post Created Successfully!")
    else:
        print("Invalid Access Token!!")
