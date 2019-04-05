from django.db import models
from django.utils import timezone


# Create your models here.
class Model(models.Model):
    model_title = models.CharField(max_length=200)
    model_content = models.TextField()
    model_published = models.DateTimeField("date published", default=timezone.now)

    def __str__(self):
        return self.model_title
