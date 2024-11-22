from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import *


urlpatterns = [
    path('<int:id>/', TagView.as_view()), #tag/id/ to delete a ceratain tag
    path('new/', TagView.as_view()), #tag/new/ to create a new tag
    path('list/', MultipleTagView.as_view()),
]