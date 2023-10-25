from django.db import models
import uuid

# Create your models here.
class Token(models.Model):
    type = models.CharField(max_length=255, null=False, blank=False, unique=True)
    token = models.TextField(unique=True) 
    
        
    def __str__(self):
        return f"{self.type}"