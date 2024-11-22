from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import *


urlpatterns = [
    path('<int:id>/', ChapterView.as_view()), #chapters/id/ for geneeral RUD
    path('new/', ChapterView.as_view()), #chapters/new/ to create a new chapter
    path('story/<int:storyid>/', ChaptersOfStoryView.as_view()), #chapters/story/id/ 
    path('latest/', LastChaptersView.as_view()), #chapters/ 
]