from rest_framework import serializers
from .models import News
from django.contrib.auth import get_user_model

User = get_user_model()

class NewsSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = News
        fields = ['id', 'type', 'title', 'url', 'content', 'created_at', 'author']
        extra_kwargs = {
            'author': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
