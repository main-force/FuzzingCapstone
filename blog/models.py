from django.db import models


class Post(models.Model):
    body = models.TextField()

    def __str__(self):
        return self.body[:50]


class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()

    def __str__(self):
        return self.body[:50]
