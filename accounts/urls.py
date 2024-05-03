from django.urls import path
from .views import UserJoinView

urlpatterns = [
    path("", UserJoinView.as_view()),
    
]
