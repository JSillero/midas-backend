from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import *


urlpatterns = [
    # review/id/ intereact with reviews
    path('<int:id>/', ReviewView.as_view()),
    path('new/', ReviewView.as_view()),  # review/new/ to create a new review
    path('story/<int:story_id>/', MultipleReviewView.as_view()),  # review/story/id
    # review/new/ to create a new review
    path('latest/', LatestReviewsView.as_view()),

]
