from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', SignInView.as_view()),
    path('delete/<int:id>/', RetrieveDestroyUserView.as_view()),
    path('<int:id>/', RetrieveDestroyUserView.as_view()),
    path('<int:userId>/addFollow/<int:storyId>/',  AddFollow.as_view()),
    path('<int:userId>/removeFollow/<int:storyId>/',  RemoveFollow.as_view()),
]
