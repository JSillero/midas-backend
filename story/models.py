from django.db import models
from tag.models import Tag

# Create your models here.


class Story(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        to='user.User',
        related_name='author_story',
        on_delete=models.CASCADE)
    cover = models.CharField(max_length=500,null=True,default="") #string which contains the url for the image
    description = models.TextField(null=True, default="")
    tags = models.ManyToManyField(
        to="tag.Tag",
        related_name='story_tag',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)