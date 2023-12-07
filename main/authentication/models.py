from django.db import models
from base.models import BaseModel
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Token(BaseModel):
    type = models.CharField(max_length=255, null=False, blank=False, unique=True)
    token = models.TextField(unique=True) 
        
    def __str__(self):
        return f"{self.type}"
    
class AuthServiceConfiguration(BaseModel):
    name=models.CharField(max_length=255, null=False, blank=False, unique=True)
    meta=models.JSONField()

    def __str__(self):
        return f"{self.name}"
