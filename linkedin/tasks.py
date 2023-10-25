from __future__ import absolute_import, unicode_literals
import requests
import json
from celery import shared_task
from datetime import datetime
from django.utils import timezone
from linkedin.models import LinkedinPost

@shared_task(name='daily_linkedin_post')
def daily_linkedin_post():
    # Get today's date
    today = timezone.now().date()

    # Try to get or create the LinkedinPost for today
    daily_linkedin_post, created = LinkedinPost.objects.get_or_create(created_at__date=today, defaults={'markdown': 'test'})

    # Provide feedback based on whether the post was created or already existed
    if created:
        print("Linkedin Post Created Successfully!")
    else:
        print(f"Linkedin Post Already created on {today.strftime('%B %d, %Y')}")

        