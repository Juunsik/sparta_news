from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint

# Create your models here.
class User(AbstractUser):
    description=models.TextField(max_length=300, blank=True)  
    
    def __str__(self):
        return self.username
    
    

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        UniqueConstraint(fields=['follower', 'followed'], name='unique_follower')