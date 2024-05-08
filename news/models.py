from django.db import models
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