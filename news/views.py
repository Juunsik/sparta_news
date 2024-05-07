from rest_framework.views import APIView
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class CommentGetPost(APIView):
    def get(self, request):
        comment = Comment.objects.all()
        serializer =CommentSerializer(comment, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "인증이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer =CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentPutDelete(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get_object(self, commentpk):
        return get_object_or_404(Comment, commentid=commentpk)

    def put(self, request, commentpk):
        comment = self.get_object(commentpk)
        if comment.user != request.user and not request.user.is_superuser:
            return Response({"error": "작성자만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def delete(self, request, commentpk):
        comment = self.get_object(commentpk)
        if comment.user != request.user and not request.user.is_superuser:
            return Response({"error": "작성자만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        data = {"delete": f"댓글 ({commentpk})번이 삭제되었습니다."}
        return Response(data, status=status.HTTP_204_NO_CONTENT)