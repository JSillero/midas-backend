from rest_framework.serializers import ModelSerializer
from .models import Story
from user.serializer import UserSerializer
from tag.serializer import TagSerializer


class StorySerializer(ModelSerializer):

    class Meta:
        model = Story
        fields = '__all__'


class PopulatedChapterSerializer(StorySerializer):
    author = UserSerializer()
    tags = TagSerializer()
