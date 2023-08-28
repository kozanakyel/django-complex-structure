from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    # for CASCADE if the user deleted, then all the blogs for user deleted
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_post")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )

    class Meta:
        ordering = ["-publish"]  # it is good or not  i think!!1
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title
