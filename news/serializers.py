from rest_framework import serializers
from .models import News, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class NewsSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    likes_count = serializers.SerializerMethodField() 

    class Meta:
        model = News
        fields = ['id', 'type', 'title', 'url', 'content', 'created_at', 'author', 'likes_count']
        extra_kwargs = {
            'author': {'read_only': True}
        }
        
    def get_likes_count(self, obj):
        return obj.likes.count()

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ["content", "created_at", "updated_at", "user"]
        
    def get_user(self, obj):
        return obj.user.username
        
    def create(self, validated_data):
        news_pk = self.context.get('view').kwargs.get('news_pk')
        news = News.objects.get(id=news_pk)
        validated_data['news'] = news
        return super().create(validated_data)

