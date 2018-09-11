from django import forms
from .models import article, author, comment,category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class createForm(forms.ModelForm):
    class Meta:
        model=article
        fields=[
            'title',
            'body',
            'image',
            'category',
        ]

class registerUser(UserCreationForm):
    class Meta:
        model=User
        fields=[
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        ]

class createauthor(forms.ModelForm):
    class Meta:
        model=author
        fields=[
            'profile_pic',
            'details',
        ]

class commentform(forms.ModelForm):
    class Meta:
        model=comment
        fields=[
            'name',
            'email',
            'post_comment'
        ]

class categoryForm(forms.ModelForm):
    class Meta:
        model=category
        fields=[
            'name'
        ]