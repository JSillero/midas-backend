from rest_framework.serializers import ModelSerializer
from .models import Review
from user.serializer import UserSerializer
from story.serializer import StorySerializer

class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        
class PopulatedReviewSerializer(ReviewSerializer):
    story =  StorySerializer() #populate the story 
    author = UserSerializer() #populate the user