from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import Follow, User
from django.db.models import Q
from .serializers import UserSerializer, UserDetailSerializer, UserUpdateSerializer, FollowSerializer
from rest_framework.permissions import IsAuthenticated

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
        


class FollowListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(Q(followed=user) | Q(follower=user))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        followers = queryset.filter(followed=request.user)
        following = queryset.filter(follower=request.user)
        followers_serializer = self.get_serializer(followers, many=True)
        following_serializer = self.get_serializer(following, many=True)
        return Response({
            'followers': followers_serializer.data,
            'following': following_serializer.data
        })

class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, username):
        
        followed_user = get_object_or_404(User, username=username)
        if request.user == followed_user:
            return Response({"detail": "자기 자신을 팔로우 할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 팔로우 관계 확인
        follow_exist = Follow.objects.filter(follower=request.user, followed=followed_user).exists()

        if follow_exist:
            # 이미 팔로우한 경우 언팔로우
            Follow.objects.filter(follower=request.user, followed=followed_user).delete()
            return Response({"detail": f"유저({followed_user})와 언팔로우했습니다."}, status=status.HTTP_200_OK)
        else:
            # 팔로우
            follow_data = {'follower': request.user.id, 'followed': followed_user.id}
            serializer = FollowSerializer(data=follow_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

