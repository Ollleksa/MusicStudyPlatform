from django.db import models
from django.conf import settings


class Lesson(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    header_image = models.ImageField(upload_to='media/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lessons'

    def __str__(self):
        return self.title


class Like(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes_on_lessons'
        unique_together = ['lesson', 'user']

        