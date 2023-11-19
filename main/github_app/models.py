from collections.abc import Iterable
from django.db import models


# Create your models here.
# class LeetCodeQuestions(models.Model):
#     title = models.CharField(max_length=255, required=True, unique=True)
#     slug = models.CharField(max_length=255, required=True, unique=True)
#     questions = models.TextField(required=True)
#     published_at = models.DateField()
#     created_at = models.DateField()
#     link = models.URLField(required=True)

    # def save(
    #     self,
    #     force_insert: bool = ...,
    #     force_update: bool = ...,
    #     using: str | None = ...,
    #     update_fields: Iterable[str] | None = ...,
    # ) -> None:
    #     return super().save(force_insert, force_update, using, update_fields)
