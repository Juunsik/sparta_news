from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsListAPIView.as_view(), name='news-list'),
<<<<<<< HEAD
    path('<int:news_pk>/', views.NewsDetailAPIView.as_view(), name='news-detail'),
    path("<int:news_pk>/comments/", views.CommentGetPost.as_view()),
    path("comments/<int:comment_pk>/", views.CommentPutDelete.as_view()),
=======
    path('<int:pk>/', views.NewsDetailAPIView.as_view(), name='news-detail'),
    path("<int:new_pk>/comments/", views.CommentGetPost.as_view()),
    path("<int:new_pk>/comments/<int:comment_pk>/", views.CommentPutDelete.as_view()),
>>>>>>> c8b145df01f23b815d61c68b6f1a6dde2d6f8e30
]
