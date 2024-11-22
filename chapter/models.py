from django.db import models
from django.utils import timezone
# Create your models here.

class Chapter (models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=500000)
    author_notes = models.TextField(max_length=10000, null=True)  # nullable
    story = models.ForeignKey(to='story.Story',
                              related_name='chapter_story',
                              on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Perform the usual action for save
        super().save(*args, **kwargs)

        # Update the father story to current time when a new chapter is added
        self.story.updated_at = timezone.now()
        self.story.save()
