from rest_framework.views import APIView
from .models import Tag
from .serializer import TagSerializer
from rest_framework.response import Response
from utils.exceptions import handle_exceptions
from rest_framework import status
from rest_framework.permissions import  IsAuthenticated
Tag_model = Tag

# Create your views here.
class TagView(APIView):
    permission_classes = [IsAuthenticated]
    
    @handle_exceptions
    def post(self, request):
        new_tag = TagSerializer(data=request.data)
        new_tag.is_valid(raise_exception=True)
        new_tag.save()
        return Response({
            'message': 'Tag creation successful',
            'tag': new_tag.data
        })
        
    @handle_exceptions
    def delete(self, request, id):
        tag = Tag_model.objects.get(pk=id)
        serialized_tag = TagSerializer(tag)
        #check if the author is the user deleting
         
        if(not request.user.is_staff):
            return Response({
                'message': 'User has no permission.',
            },status=status.HTTP_403_FORBIDDEN)
        
        tag.delete()
        return Response({
            'message': 'Tag deleted.',
            'story': serialized_tag.data
        },status=status.HTTP_204_NO_CONTENT)

class MultipleTagView(APIView):
    
    @handle_exceptions
    def get(self,request):
        tags =Tag_model.objects.all()
        serialized_tags = TagSerializer(tags,many=True)
        return Response({
            'tags': serialized_tags.data
        })     
