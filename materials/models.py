from django.db import models


class Course(models.Model):
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to="course_previews/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)


class Lesson(models.Model):
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    preview = models.ImageField(upload_to="lesson_previews/", blank=True, null=True)
    video_url = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")

    def __str__(self):
        return self.title
