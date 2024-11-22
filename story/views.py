from rest_framework.views import APIView
from .models import Story
from .serializer import StorySerializer

from user.models import User
from user.serializer import UserSerializer

from rest_framework.response import Response
from utils.exceptions import handle_exceptions
from rest_framework import status
from django.db.models import Q
from utils.permissions import IsOwnerOrReadOnly


Story_model = Story
# Views


class StoryView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    @handle_exceptions
    def post(self, request):
        new_story = StorySerializer(data=request.data)
        new_story.is_valid(raise_exception=True)
        new_story.save()
        return Response({
            'message': 'Story creation successful',
            'story': new_story.data
        }, status=status.HTTP_200_OK)

    @handle_exceptions
    def get(self, request, id):
        story = Story_model.objects.get(pk=id)
        serialized_story = StorySerializer(story)
        return Response({
            'story': serialized_story.data,
        }, status=status.HTTP_200_OK)

    @handle_exceptions
    def delete(self, request, id):
        story = Story_model.objects.get(pk=id)
        serialized_story = StorySerializer(story)
        # check if the author is the user deleting
        if (str(story.author) == str(request.user)):
            return Response({
                'message': 'User does not own the story.',
            }, status=status.HTTP_403_FORBIDDEN)

        story.delete()
        return Response({
            'message': 'Story deleted.',
            'story': serialized_story.data
        }, status=status.HTTP_200_OK)

    @handle_exceptions
    def put(self, request, id):
        story = Story_model.objects.get(pk=id)
        serialized_story = StorySerializer(
            story, data=request.data, partial=True)

        if (str(story.author) == str(request.user)):
            return Response({
                'message': 'User does not own the story.',
            }, status=status.HTTP_403_FORBIDDEN)

        serialized_story.is_valid(raise_exception=True)
        serialized_story.save()

        # Send response
        return Response({
            'message': 'Story edited.',
            'story': serialized_story.data
        }, status=status.HTTP_200_OK)


class StoryListByAuthorView(APIView):
    def get(self, request, authorid):
        story = Story_model.objects.filter(Q(author__id=authorid))
        serialized_story = StorySerializer(story, many=True)

        return Response({
            'stories': serialized_story.data
        }, status=status.HTTP_200_OK)


class GetStories(APIView):
    def get(self, request):
        stories = Story_model.objects.prefetch_related(
            'tags').order_by('updated_at')
        serialized_stories = StorySerializer(stories, many=True)

        return Response({
            'stories': serialized_stories.data
        })


class GetStoriesByQuery(APIView):
    def post(self, request):
        query = request.data
        print(query)
        stories = Story_model.objects.prefetch_related(
            'tags').filter(Q(title__contains=query['title']), Q(author__username__contains=query['author']), Q(description__contains=query['description'])).order_by('updated_at')
        serialized_stories = StorySerializer(stories, many=True)

        return Response({
            'stories': serialized_stories.data
        })


class GetLastStories(APIView):
    def get(self, request):
        stories = Story_model.objects.prefetch_related(
            'tags').order_by('updated_at')[:10]
        serialized_stories = StorySerializer(stories, many=True)

        return Response({
            'stories': serialized_stories.data
        })


class GetFollowedStories(APIView):
    def get(self, request, userId):
        user = User.objects.get(pk=userId)
        serialized_user = UserSerializer(user)
        follows = serialized_user.data['follows']

        stories = Story_model.objects.filter(pk__in=follows)
        serialized_stories = StorySerializer(stories, many=True)

        return Response({
            'stories': serialized_stories.data
        })
