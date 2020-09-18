from django.db import models


class Tweet(models.Model):
    """Add user inputted tweet to the database."""
    # id = models.AutoField(primary_key=True)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
