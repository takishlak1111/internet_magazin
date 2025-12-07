from django import forms
from django.contrib.auth.forms import AuthenticationForm

from internet_magazin.users.models import User


class UserLoginForm(forms.ModelForm ):
    class Meta:
        model = User 