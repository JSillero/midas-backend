from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import *

urlpatterns = [
    path('<int:id>/', StoryView.as_view()),  # stories/id/ to get a story by id
    path('new/', StoryView.as_view()),  # stories/new/ basic crud for stories
    # story/author/id/
    path('author/<int:authorid>/', StoryListByAuthorView.as_view()),# stories/author/authorid
    path('/', GetStories.as_view()),  # stories/ returns all stories
    path('latest/', GetLastStories.as_view()),  # stories/ returns newest 10 stories
    path('search/', GetStoriesByQuery.as_view()),
    path('followed/<int:userId>/', GetFollowedStories.as_view()),# stories/followed/id returns stories with pk contained in user__follows
]
