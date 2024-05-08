from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
<<<<<<< HEAD
=======
    pass
>>>>>>> 533891b914931f4f6b9035234547749b501e5e5f
    description=models.TextField(max_length=300, blank=True)
    
    def __str__(self):
        return self.username