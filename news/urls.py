from django.urls import path
from . import views
from .news_generator import GenerateNews

urlpatterns = [
    path("", views.NewsListAPIView.as_view(), name="news-list"),
    path("<int:news_pk>/", views.NewsDetailAPIView.as_view(), name="news-detail"),
    path("<int:news_pk>/comments/", views.CommentGetPost.as_view()),
    path("comments/<int:comment_pk>/", views.CommentPutDelete.as_view()),
    path("ai/", GenerateNews.as_view()),
]
