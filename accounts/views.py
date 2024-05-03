from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer

# Create your views here.


class UserJoinView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
