from rest_framework.views import APIView
from .models import Comment, News
from .serializers import CommentSerializer, NewsSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status

# Create your views here.
class NewsListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

    def post(self, request):
        """뉴스 작성하기"""
        serializer = NewsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            if request.user.is_authenticated:
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "로그인이 필요한 작업입니다."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class NewsDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, news_pk):
        news = get_object_or_404(News, pk=news_pk)
        serializer = NewsSerializer(news)
        return Response(serializer.data)

    def put(self, request, news_pk):
        news = get_object_or_404(News, pk=news_pk)
        serializer = NewsSerializer(news, data=request.data, partial=True)
        if serializer.is_valid():
            if request.user.is_authenticated and news.author == request.user:
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"detail": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, news_pk):
        news = get_object_or_404(News, pk=news_pk)
        if request.user.is_authenticated and news.author == request.user:
            news.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class CommentGetPost(APIView):
    def get(self, request, news_pk):
        news = News.objects.get(id=news_pk)
        comments = news.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, news_pk):
        if not request.user.is_authenticated:
            return Response({"error": "인증이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = CommentSerializer(data=request.data, context={'view': self})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentPutDelete(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get_object(self, comment_pk):
        return get_object_or_404(Comment, pk=comment_pk)

    def put(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        if comment.user != request.user and not request.user.is_superuser:
            return Response({"error": "작성자만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def delete(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        if comment.user != request.user and not request.user.is_superuser:
            return Response({"error": "작성자만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        data = {"delete": f"댓글 ({comment_pk})번이 삭제되었습니다."}
        return Response(data, status=status.HTTP_204_NO_CONTENT)


