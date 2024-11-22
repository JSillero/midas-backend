# Generated by Django 5.1.3 on 2024-11-18 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0001_initial'),
        ('user', '0002_user_bio_user_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='follows',
            field=models.ManyToManyField(blank=True, related_name='user_follows', to='story.story'),
        ),
    ]
