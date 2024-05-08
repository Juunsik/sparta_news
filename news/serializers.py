from rest_framework import serializers
<<<<<<< HEAD
from .models import Comment
=======
>>>>>>> c8b145df01f23b815d61c68b6f1a6dde2d6f8e30
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
<<<<<<< HEAD
    
    
    
    
=======
from .models import Comment

>>>>>>> c8b145df01f23b815d61c68b6f1a6dde2d6f8e30
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

<<<<<<< HEAD


    
=======
>>>>>>> c8b145df01f23b815d61c68b6f1a6dde2d6f8e30
