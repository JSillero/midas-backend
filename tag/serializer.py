from rest_framework.serializers import ModelSerializer
from .models import Tag
from user.serializer import UserSerializer

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        
