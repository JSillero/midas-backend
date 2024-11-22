from rest_framework.views import APIView
from .models import Comment
from .serializer import CommentSerializer
from rest_framework.response import Response
from utils.exceptions import handle_exceptions
from rest_framework import status
from django.db.models import Q
from utils.permissions import IsOwnerOrReadOnly


Comment_model = Comment
# Views


class CommentView(APIView):
    
    @handle_exceptions
    def get(self, request,id):
        comment = Comment_model.objects.get(pk=id)
        serialized_comment = CommentSerializer(comment)
        return Response({
            'comment': serialized_comment.data
        })
    
    @handle_exceptions
    def post(self, request):
        print(request.data)
        if(request.user.id == request.data['commenter']):
            new_comment = CommentSerializer(data=request.data)
            new_comment.is_valid(raise_exception=True)
            new_comment.save()
            return Response({
                'message': 'Comment creation successful',
                'comment': new_comment.data
            })
            
        return Response({
            'message': 'User has no permission.',
        }, status=status.HTTP_403_FORBIDDEN)
        
    @handle_exceptions
    def put(self, request,id):
        comment = Comment_model.objects.get(pk=id)
        
        #if user is staff or user owns the comment
        if (request.user.is_staff or (comment.commenter == str(request.user))):
            serialized_comment = CommentSerializer(
                comment, data=request.data, partial=True)
            serialized_comment.is_valid(raise_exception=True)
            serialized_comment.save()
            return Response({
                'message': 'Comment edited.',
                'chapter': serialized_comment.data
            })

        return Response({
            'message': 'User has no permission.',
        }, status=status.HTTP_403_FORBIDDEN)
    
    @handle_exceptions
    def delete(self, request,id):
        comment = Comment_model.objects.get(pk=id)
        serialized_comment = CommentSerializer(comment)
        
        if ( request.user.is_staff or (str(comment.commenter) == str(request.user))):
            comment.delete()
            return Response({
            'message': 'Chapter deleted.',
            'chapter': serialized_comment.data
            }, status=status.HTTP_204_NO_CONTENT)
            
        return Response({
            'message': 'User has no permission.',
        }, status=status.HTTP_403_FORBIDDEN)

class CommentListView(APIView):
    def get(self,request,chapterid):
        comments = Comment_model.objects.filter(Q(chapter__id=chapterid))
        serialized_comment = CommentSerializer(comments, many=True )
 
        return Response({
            'chapter': serialized_comment.data
            }, status=status.HTTP_204_NO_CONTENT)
        