from django.db import models
from base.models import BaseModel

# Create your models here.
class Token(BaseModel):
    type = models.CharField(max_length=255, null=False, blank=False, unique=True)
    token = models.TextField(unique=True) 
        
    def __str__(self):
        return f"{self.type}"