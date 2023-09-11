from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    topic = models.CharField(max_length=150)

    def __str__(self):
        return self.topic


class Feed(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="uploads/")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(
        Feed, on_delete=models.CASCADE, related_name="commented_feed"
    )
    comment_body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.comment_body[:50]
