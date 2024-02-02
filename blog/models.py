from django.db import models
from django.urls import reverse

class Post(models.Model):
    """Post Model Class"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="posts",
    )
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String method"""
        return self.title
    
    def get_absolute_url(self):
        """Get the absolute URL for a single post"""
        return reverse("post_detail", kwargs={"pk":self.pk})
