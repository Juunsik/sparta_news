from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsListAPIView.as_view(), name='news-list'),
    path('<int:pk>/', views.NewsDetailAPIView.as_view(), name='news-detail'),
    path("<int:new_pk>/comments/", views.CommentGetPost.as_view()),
    path("<int:new_pk>/comments/<int:comment_pk>/", views.CommentPutDelete.as_view()),
]
