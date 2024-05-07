from django.urls import path
from .views import NewsDetailAPIView, NewsListAPIView

urlpatterns = [
    path('', NewsListAPIView.as_view(), name='news-list'),
    path('<int:pk>/', NewsDetailAPIView.as_view(), name='news-detail')
]