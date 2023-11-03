from django.db import models
from base.models import BaseModel

# Create your models here.
class DatabaseBackup(BaseModel):
    url = models.URLField(blank=False, null=False)

    def __str__(self):
        return f"{self.created_at.strftime('%B %d, %Y')}"