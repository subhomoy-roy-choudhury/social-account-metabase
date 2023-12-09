from django.db import models
from base.models import BaseModel

# Create your models here.
class Tweet(BaseModel):
    markdown = models.TextField(null=False, blank=False)
    tweet_id = models.CharField(max_length=255, null=False, blank=True)
    is_send = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} --- {self.tweet_id}"