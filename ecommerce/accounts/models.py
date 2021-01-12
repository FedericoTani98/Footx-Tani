import json
import string
from core.models import Item
from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


# Create your models here.





# Il modello che registra i dati dell'utente nel sito
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    item = models.ManyToManyField(Item)


    def __str__(self):
        return self.user.username


