from django.db import models
<<<<<<< HEAD
from django.conf import settings
=======
>>>>>>> c8b145df01f23b815d61c68b6f1a6dde2d6f8e30
from django.contrib.auth import get_user_model

# Create your models here.

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
<<<<<<< HEAD


=======
from django.conf import settings

>>>>>>> c8b145df01f23b815d61c68b6f1a6dde2d6f8e30

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments")
    
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.content
<<<<<<< HEAD

=======
>>>>>>> c8b145df01f23b815d61c68b6f1a6dde2d6f8e30
