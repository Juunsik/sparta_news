from django.db import models
<<<<<<< HEAD
from django.conf import settings

# Create your models here.


class Comment(models.Model):
    News = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments")
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.content
=======
from django.contrib.auth import get_user_model

User = get_user_model()

class News(models.Model):
    type = models.CharField(max_length=100)  
    title = models.CharField(max_length=255)  
    url = models.URLField()  
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_posts')  

    def __str__(self):
        return self.title
>>>>>>> 533891b914931f4f6b9035234547749b501e5e5f
