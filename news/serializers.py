from rest_framework import serializers
from .models import Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content", "created_at", "updated_at"]

