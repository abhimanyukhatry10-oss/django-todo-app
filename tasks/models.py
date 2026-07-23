from django.db import models

from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True) #blank=True ka matlab ye field optional hai.
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
# Create your models here.
