from django.db import models

# Create your models here.
class Comment(models.Model):
    commenter = models.ForeignKey(
        to='user.User',
        related_name='author_comment',
        on_delete=models.CASCADE)
    content = models.TextField(max_length=30000)
    chapter= models.ForeignKey(
        to='chapter.Chapter',
        related_name='chapter_story',
        on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)