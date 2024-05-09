from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, UserDetailSerializer, UserUpdateSerializer, FollowSerializer

# Create your views here.


class UserJoinView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):
    
    def get_object(self, username):
        return get_object_or_404(get_user_model(), username=username)
        
    
    def get(self, request, username):
        user=self.get_object(username)
        serializer=UserDetailSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, username):
        password=request.data.get('password')
        password2=request.data.get('password2')
        if (password or password2) and (password!=password2):
            return Response({'error':"password or password2 not exist or password is not equal"}, status=status.HTTP_400_BAD_REQUEST)
        
        user=self.get_object(username)
        serializer=UserDetailSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            user=serializer.save()
            if password:
                user.set_password(password)
                user.save()
            serializer=UserUpdateSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        



class FollowAPIView(APIView):
    def get(self, request):
        user = request.user
        followings = Follow.objects.filter(follower=user)
        serializer = FollowSerializer(followings, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        followed_id = request.data.get('followed_id')
        try:
            followed_user = User.objects.get(id=followed_id)
        except User.DoesNotExist:
            return Response({'error': '유저를 찾지 못했습니다'}, status=status.HTTP_404_NOT_FOUND)
        
        if followed_user == user:
            return Response({'error': '자기 자신은 팔로우하실수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            follow_instance = Follow.objects.get(follower=user, followed=followed_user)
            follow_instance.delete()
            return Response({'message': f'({followed_user})님을 언팔로우 하셨습니다.'}, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            follow_instance = Follow.objects.create(follower=user, followed=followed_user)
            serializer = FollowSerializer(follow_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)