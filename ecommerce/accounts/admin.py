from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model

from accounts.models import UserProfile

User = get_user_model()
'''
abbiamo registrato il nostro modello UserProfile
'''
admin.site.register(UserProfile)
