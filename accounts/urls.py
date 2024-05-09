from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
    )
from . import views

urlpatterns = [
    path("", views.UserJoinView.as_view()),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("<str:username>/",views.UserDetailAPIView.as_view()),
    path('follow/<user_id>/', views.FollowAPIView.as_view(), name='follow'),
]
