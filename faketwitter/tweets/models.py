import random
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Tweet(models.Model):
    """Add user inputted tweet to the database.

    Maps to SQL data
    """
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    # TODO: remove default=1, default user - Jankey. (Means anyone can tweet
    # without logging in.)

    # Multiple user tweets (ForeignKey)
    # Set to models.CASCADE if SET_NULL is causing issues (del null=True)
    # CASCADE, if user is deleted, all tweets will be deleted

    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 999)
        }
