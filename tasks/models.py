from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200) #Isliye CharField ka relation SQL ke VARCHAR se hota hai.
    #CharField me max_length mandatory hai.
    description = models.TextField(blank=True) #description is optional

    completed = models.BooleanField(default=False)

    PRIORITY_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),]

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="Medium",
    )

    due_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
# Create your models here.
