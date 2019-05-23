from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from PIL import Image

from .models import PlatformUser


class PlatformUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = PlatformUser
        fields = ('username', 'email', 'avatar')


class PlatformUserChangeForm(UserChangeForm):

    class Meta:
        model = PlatformUser
        fields = ('username', 'email')


class PlatformAuthForm(AuthenticationForm):
    pass


class AvatarForm(forms.ModelForm):

    class Meta:
        model = PlatformUser
        fields = ('avatar', )

    def save(self):
        avatar= super(AvatarForm, self).save()

        image = Image.open(avatar.avatar)
        cropped_image = image.thumbnail((128,128))
        cropped_image.save(avatar.avatar.path)

        return avatar