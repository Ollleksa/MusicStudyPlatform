from django.db import models
from django.conf import settings

from django.core.exceptions import ValidationError


class Request(models.Model):
    requestor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title



