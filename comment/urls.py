from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import *

urlpatterns = [
    path('<int:id>/', CommentView.as_view()), #story/id/ to get a story by id
    path('new/', CommentView.as_view()), #story/new/ basic crud for stories
    path('chapter/<int:chapterid>/', CommentListView.as_view()),
    # path('delete/<int:id>/', RetrieveDestroyUserView.as_view()),
    # path('signin/', SignInView.as_view())
]
