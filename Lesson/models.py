from django.db import models
from django.conf import settings


class Lesson(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Like', related_name='likes_on_lesson')
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lessons'

    def __str__(self):
        return self.title


class Like(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    #is_liked = models.BooleanField(default=True)

    class Meta:
        db_table = 'likes_on_lessons'
        