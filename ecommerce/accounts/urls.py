"""account URL Configuration"""
from django.contrib.auth.decorators import login_required
from django.urls import path

from .import views
from .views import registrazioneView

urlpatterns = [
    path('registrazione/', registrazioneView, name='registration_view'),

]
