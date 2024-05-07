from rest_framework.views import APIView
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class CommentGetPost(APIView):
    def get(self, request, news_id):
        news = News.objects.get(id=news_id)
        comments = news.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, news_id):
        if not request.user.is_authenticated:
            return Response({"error": "인증이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = CommentSerializer(data=request.data, context={'view': self})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentPutDelete(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get_object(self, comment_pk):
        return get_object_or_404(Comment, commentid=comment_pk)

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