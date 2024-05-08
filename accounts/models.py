from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
<<<<<<< HEAD
    description=models.TextField(max_length=300, blank=True)  
=======
    description=models.TextField(max_length=300, blank=True)
>>>>>>> c8b145df01f23b815d61c68b6f1a6dde2d6f8e30
    
    def __str__(self):
        return self.username