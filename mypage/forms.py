from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def validate_email(value):
    if User.objects.filter(email = value).exists():
        raise ValidationError((f"{value} 는 이미 있는 이메일 입니다."),params = {'value':value})

class UserForm(UserCreationForm):
    email = forms.EmailField(validators = [validate_email])

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']