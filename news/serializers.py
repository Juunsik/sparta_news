from rest_framework import serializers
<<<<<<< HEAD
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content", "created_at", "updated_at"]
        
    def create(self, validated_data):
        news_id = self.context.get('view').kwargs.get('news_id')
        news = News.objects.get(id=news_id)
        validated_data['news'] = news
        return super().create(validated_data)

=======
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
>>>>>>> 533891b914931f4f6b9035234547749b501e5e5f
