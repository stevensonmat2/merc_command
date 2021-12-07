from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=30)
