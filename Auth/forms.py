from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from .models import PlatformUser


class PlatformUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = PlatformUser
        fields = ('username', 'email', 'is_teacher')


class PlatformUserChangeForm(UserChangeForm):

    class Meta:
        model = PlatformUser
        fields = ('username', 'email', 'is_teacher')


class PlatformAuthForm(AuthenticationForm):
    pass
