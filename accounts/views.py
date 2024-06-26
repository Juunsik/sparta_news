from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import Follow, User
from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
    FollowSerializer,
)
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

# Create your views here.


class UserJoinView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def get_object(self, username):
        return get_object_or_404(get_user_model(), username=username)

    def get(self, request, username):
        user = self.get_object(username)
        if user!=request.user:
            return Response({'error': "You do not have permission to query."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    def put(self, request, username):
        user = self.get_object(username)
        if user!=request.user:
            return Response({'error': "You do not have permission to query."}, status=status.HTTP_401_UNAUTHORIZED)
        password = request.data.get("password")
        password2 = request.data.get("password2")
        if (password or password2) and (password != password2):
            return Response(
                {"error": "password or password2 not exist or password is not equal"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = UserDetailSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            user = serializer.save()
            if password:
                user.set_password(password)
                user.save()
            serializer = UserUpdateSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class FollowListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        username = kwargs.get("username")
        user = get_object_or_404(User, username=username)
        following = list(
            Follow.objects.filter(follower=user).values_list(
                "followed__username", flat=True
            )
        )
        followers = list(
            Follow.objects.filter(followed=user).values_list(
                "follower__username", flat=True
            )
        )
        data = {"following": following, "followers": followers}
        return JsonResponse(
            data, json_dumps_params={"ensure_ascii": False}, status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        username = kwargs.get("username")
        followed_user = get_object_or_404(User, username=username)

        if request.user == followed_user:
            return Response(
                {"detail": "자기 자신을 팔로우 할 수 없습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow_exist = Follow.objects.filter(
            follower=request.user, followed=followed_user
        ).exists()

        if follow_exist:
            Follow.objects.filter(
                follower=request.user, followed=followed_user
            ).delete()
            return Response(
                {"detail": f"유저({followed_user})와 언팔로우했습니다."},
                status=status.HTTP_200_OK,
            )
        else:
            follow_data = {"follower": request.user.id, "followed": followed_user.id}
            serializer = FollowSerializer(data=follow_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
