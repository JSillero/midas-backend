from django.db import models

# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=500000)
    author = models.ForeignKey(to='user.User',
        related_name='author_review',
        on_delete=models.CASCADE) 
    story = models.ForeignKey(to='story.Story',
        related_name='story_review',
        on_delete=models.CASCADE)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:     
        unique_together = ('story', 'author',)