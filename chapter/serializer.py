from rest_framework.serializers import ModelSerializer
from .models import Chapter
from user.serializer import UserSerializer

class ChapterSerializer(ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'
        
class PopulatedChapterSerializer(ChapterSerializer):
    story = UserSerializer() #populate the story 