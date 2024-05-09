import json
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Q
from accounts.models import User
from .models import Comment, News
from .serializers import CommentSerializer, NewsSerializer
from .news_generator import GenerateNews
from .pagination import PaginationHandlerMixin


# Create your views here.
class NewsPagination(PageNumberPagination):
    page_size = 10


class NewsListAPIView(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = NewsPagination

    def get(self, request):
        if request.GET.get("type") == "weekly":
            news = (
                News.objects.filter(Q(type="news") | Q(type="show") | Q(type="plus"))
                .annotate(likes_count=Count("likes"))
                .order_by("-likes_count")[:20]
            )
        elif request.GET.get("type") == "plus":
            news = News.objects.filter(type="plus").order_by("-created_at")
        elif request.GET.get("type") == "ask":
            news = News.objects.filter(type="ask").order_by("-created_at")
        elif request.GET.get("type") == "show":
            news = News.objects.filter(type="show").order_by("-created_at")
        elif request.GET.get("type") is None:
            news = News.objects.all().order_by("-created_at")

        page = self.paginate_queryset(news)
        if page is not None:
            serializer = self.get_paginated_response(
                NewsSerializer(page, many=True).data
            )
        else:
            serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NewsSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            news = serializer.save(author=request.user)
            if news.type == "ask":
                news.url = ""
                news.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentGetPost(APIView):
    def get(self, request, news_pk):
        news = News.objects.get(id=news_pk)
        comments = news.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, news_pk):
        if not request.user.is_authenticated:
            return Response(
                {"error": "인증이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = CommentSerializer(data=request.data, context={"view": self})
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
            return Response(
                {"error": "작성자만 수정할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        if comment.user != request.user and not request.user.is_superuser:
            return Response(
                {"error": "작성자만 삭제할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )
        comment.delete()
        data = {"delete": f"댓글 ({comment_pk})번이 삭제되었습니다."}
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class LikeNews(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, news_pk):
        news = get_object_or_404(News, pk=news_pk)
        if news.likes.filter(pk=request.user.pk).exists():
            news.likes.remove(request.user)
            return Response({"likes": news.likes.count()}, status=status.HTTP_200_OK)
        else:
            news.likes.add(request.user)
        return Response({"likes": news.likes.count()}, status=status.HTTP_200_OK)


class LikedNews(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        liked_news = News.objects.filter(likes=request.user)
        serializer = NewsSerializer(liked_news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.likes.filter(pk=request.user.pk).exists():
            comment.likes.remove(request.user)
            return Response({"likes": comment.likes.count()}, status=status.HTTP_200_OK)
        else:
            comment.likes.add(request.user)
        return Response({"likes": comment.likes.count()}, status=status.HTTP_200_OK)


class LikedComments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        liked_comments = Comment.objects.filter(likes=request.user)
        serializer = CommentSerializer(liked_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AIGenerateNews(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        res = GenerateNews()

        if res.status_code == 200:
            generated_data = res.json()
            news_data = json.loads(generated_data["choices"][0]["message"]["content"])
            admin_user = User.objects.get(username="admin")

            serializer = NewsSerializer(
                data={
                    "type": "plus",
                    "title": news_data["title"],
                    "content": news_data["content"],
                    "url": news_data["url"],
                },
                context={"request": request},
            )
            if serializer.is_valid():
                news = serializer.save(author_id=admin_user.pk)
                news.title = "GN+:" + news.title
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "Failed to generate story from AI"},
                status=res.status_code,
            )
