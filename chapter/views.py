from rest_framework.views import APIView
from .models import Chapter
from story.models import Story
from .serializer import ChapterSerializer
from rest_framework.response import Response
from utils.exceptions import handle_exceptions
from rest_framework import status
from pprint import pprint
from django.db.models import Q

# Create your views here.

Chapter_model = Chapter
Story_model = Story


class ChapterView(APIView):
    @handle_exceptions
    def get(self, request, id):
        chapter = Chapter_model.objects.get(pk=id)
        serialized_chapter = ChapterSerializer(chapter)
        return Response({
            'chapter': serialized_chapter.data
        })

    @handle_exceptions
    def post(self, request):
        new_chapter = ChapterSerializer(data=request.data)
        new_chapter.is_valid(raise_exception=True)
        new_chapter.save()
        return Response({
            'message': 'Chapter added',
            'chapter': new_chapter.data
        })

    @handle_exceptions
    def put(self, request, id):
        chapter = Chapter.objects.get(pk=id)

        if (request.user.is_staff or (chapter.story.author.username == str(request.user))):
            serialized_chapter = ChapterSerializer(
                chapter, data=request.data, partial=True)
            serialized_chapter.is_valid(raise_exception=True)
            serialized_chapter.save()
            return Response({
                'message': 'Chapter eddited.',
                'chapter': serialized_chapter.data
            })

        return Response({
            'message': 'User has no permission.',
        }, status=status.HTTP_403_FORBIDDEN)

    @handle_exceptions
    def delete(self, request, id):
        chapter = Chapter_model.objects.get(pk=id)
        serialized_chapter = ChapterSerializer(chapter)
        # check if the author is the user deleting
        print(not request.user.is_staff)
        print("comparison:", str(chapter.story.author.username) != str(request.user))
        print(str(chapter.story.author.username), str(request.user))

        if (request.user.is_staff or (chapter.story.author.username == str(request.user))):
            chapter.delete()
            return Response({
                'message': 'Chapter deleted.',
                'chapter': serialized_chapter.data
            }, status=status.HTTP_204_NO_CONTENT)

        return Response({
            'message': 'User has no permission.',
        }, status=status.HTTP_403_FORBIDDEN)


class ChaptersOfStoryView(APIView):
    @handle_exceptions
    def get(self, request, storyid):
        chapter = Chapter_model.objects.filter(
            Q(story__id=storyid)).order_by('created_at')
        serialized_chapters = ChapterSerializer(chapter, many=True)

        return Response({
            'chapters': serialized_chapters.data
        }, status=status.HTTP_200_OK)


class LastChaptersView(APIView):
    @handle_exceptions
    def get(self, request):
        chapters = Chapter_model.objects.all().order_by('-created_at')[:10]
        serialized_chapters = ChapterSerializer(chapters, many=True)

        return Response({
            'chapters': serialized_chapters.data
        }, status=status.HTTP_200_OK)
