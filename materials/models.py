from django.db import models
from django.conf import settings

class Course(models.Model):
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

class Lesson(models.Model):
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    preview = models.ImageField(upload_to='lesson_previews/', blank=True, null=True)
    video_url = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.title
