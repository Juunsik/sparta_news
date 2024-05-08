from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class News(models.Model):
    type = models.CharField(max_length=100)  
    title = models.CharField(max_length=255)  
    url = models.URLField()  
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  
    author = models.ForeignKey(User, related_name='news_posts', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_news', blank=True)  

    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments")
    
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="liked_comments", blank=True)
    

    def __str__(self):
        return self.content