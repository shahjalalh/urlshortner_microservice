from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UrlShortner(models.Model):
    user = models.ForeignKey(User)
    original_url = models.URLField(max_length=255)
    short_url = models.URLField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.original_url)
