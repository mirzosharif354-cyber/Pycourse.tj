from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'inp','placeholder':'Логин'})
        self.fields['password'].widget.attrs.update({'class':'inp','placeholder':'Парол'})
