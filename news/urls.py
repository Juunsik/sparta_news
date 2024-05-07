from django.urls import path
from . import views

urlpatterns = [
    path("api/news/<int:pk>/comments/", views.CommentGetPost.as_view()),
    path("/api/news/<int:pk>/comments/delete/", views.CommentPutDelete.as_view()),
]
