from rest_framework import serializers
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

