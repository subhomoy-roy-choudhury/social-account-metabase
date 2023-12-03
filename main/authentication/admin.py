from django.contrib import admin
from authentication.models import Token, AuthServiceConfiguration

# Register your models here.
admin.site.register(Token)
admin.site.register(AuthServiceConfiguration)