from rest_framework.views import APIView
from .models import Review
from .serializer import ReviewSerializer
from rest_framework.response import Response
from utils.exceptions import handle_exceptions
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q


Review_model = Review

# Create your views here.


class ReviewView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @handle_exceptions
    def post(self, request):
        new_review = ReviewSerializer(data=request.data)
        new_review.is_valid(raise_exception=True)
        if(new_review.validated_data['author'].id == request.user.id):
            new_review.save()
            return Response({
                'message': 'Review created.',
                'review': new_review.data
            })
            
        return Response({
            'message': 'User is not the author.',
        }, status=status.HTTP_403_FORBIDDEN)


    @handle_exceptions
    def delete(self, request, id):
        review = Review_model.objects.get(pk=id)
        serialized_tag = Review_model(review)
        # check if the author is the user deleting

        if (request.user.is_staff or (str(request.user) == str(review.author))):
            review.delete()
            return Response({
                'message': 'review deleted.',
                'review': serialized_tag.data
            }, status=status.HTTP_204_NO_CONTENT)

        return Response({
            'message': 'User has no permission.',
        }, status=status.HTTP_403_FORBIDDEN)


class MultipleReviewView(APIView):

    @handle_exceptions
    def get(self, request, story_id):
        review = Review_model.objects.filter(Q(story__id=story_id))
        serialized_reviews = ReviewSerializer(review, many=True)
        return Response({
            'reviews': serialized_reviews.data
        })

class LatestReviewsView(APIView):
    @handle_exceptions
    def get(self, request):
        review = Review_model.objects.all().order_by('-created_at')[:10]
        serialized_reviews = ReviewSerializer(review, many=True)
        return Response({
            'reviews': serialized_reviews.data
        })