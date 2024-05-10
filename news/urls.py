from django.urls import path
from . import views
from .news_generator import GenerateNews

urlpatterns = [
    path("", views.NewsListAPIView.as_view(), name="news-list"),
    path("<int:news_pk>/", views.NewsDetailAPIView.as_view(), name="news-detail"),
    path("<int:news_pk>/comments/", views.CommentGetPost.as_view()),
    path("comments/<int:comment_pk>/", views.CommentPutDelete.as_view()),
    path("gnplus/", views.AIGenerateNews.as_view()),
    path("likes/<int:news_pk>/", views.LikeNews.as_view()),
    path("likes/news/", views.LikedNews.as_view()),
    path("likes/comments/<int:comment_pk>/", views.LikeComment.as_view()),
    path("likes/comments/", views.LikedComments.as_view()),
]