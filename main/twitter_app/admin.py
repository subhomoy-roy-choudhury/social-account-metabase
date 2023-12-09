from django.contrib import admin
from twitter_app.models import Tweet

# Register your models here.
admin.site.register(Tweet)

admin.site.site_header = "Tweets"