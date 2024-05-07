from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass
    description=models.TextField(max_length=300, blank=True)
    
    def __str__(self):
        return self.username