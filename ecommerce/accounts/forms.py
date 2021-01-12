from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



'''
Classe utilizzata per estendere il form predefinito di django
assocciando un indirizzo email all'account creato
'''
class FormRegistrazione(UserCreationForm):
    email = forms.CharField(max_length=100, required=True, widget=forms.EmailInput())


'''
Classe contenete i campi che il guest deve inserire per potersi registrare
'''
class Meta:
    model = User
    fields = ['username','email','password1','password2']



