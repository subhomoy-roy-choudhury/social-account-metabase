from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from linkedin.models import LinkedinPost
from linkedin.helpers import get_linkedin_post, create_linkedin_post
from authentication.helpers import check_linkedin_token


@shared_task(name="daily_linkedin_post")
def daily_linkedin_post():
    # Get today's date
    today = timezone.now().date()

    # check Linkedin access token
    try :
        access_token, error = check_linkedin_token()
        if access_token:
                # Try to get the LinkedinPost for today
                daily_linkedin_posts_count = LinkedinPost.objects.filter(created_at__date=today).count()
                if daily_linkedin_posts_count > 0: 
                    print(f"Linkedin Post Already created on {today.strftime('%B %d, %Y')}")
                else :
                    # If post doesn't exist, then fetch the LinkedIn post and create the object
                    markdown_content = get_linkedin_post()
                    # Create Post
                    # linkedin_post_id = create_linkedin_post(access_token, markdown_content)
                    linkedin_post_id = "urn:li:share:6521244543193575424"
                    daily_linkedin_post = LinkedinPost.objects.create(
                        created_at=today,
                        markdown=markdown_content,
                        linkedin_post_id=linkedin_post_id,
                    )
                    print("Linkedin Post Created Successfully!")
        else:
            print("Invalid Access Token!!")
    except Exception as e:
         print("error in daily_linkedin_post task")
