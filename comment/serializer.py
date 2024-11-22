from rest_framework.serializers import ModelSerializer
from .models import Comment
from user.serializer import UserSerializer
from chapter.serializer import ChapterSerializer
 
class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
class PopulatedCommentSerializer(CommentSerializer):
    commenter = UserSerializer() 
    chapter = ChapterSerializer()