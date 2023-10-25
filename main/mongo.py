import pymongo
from django.conf import settings

client = pymongo.MongoClient(settings.MONGO_DATABASE)
db = client.social_account_metabase