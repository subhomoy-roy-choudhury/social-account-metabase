from django.db import models

# Create your models here.
class Token(models.Model):
    type = models.CharField(max_length=255, null=False, blank=False, unique=True)
    token = models.CharField(max_length=255, null=False, blank=False)
        
    def __str__(self):
        return f"{self.type}"