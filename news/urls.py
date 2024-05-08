from django.urls import path
from . import views

urlpatterns = [
    path("api/news/<int:new_pk>/comments/", views.CommentGetPost.as_view()),
    path("/api/news/<int:new_pk>/comments/<int:comment_pk>/", views.CommentPutDelete.as_view()),
]
