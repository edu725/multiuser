from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPES=(
        ('admin', 'Admin'),
        ('client', 'Client'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

class Itens(models.Model):
    name = models.CharField(max_length=240)
    descript = models.TextField()
    path = models.ImageField(upload_to="imagens/")