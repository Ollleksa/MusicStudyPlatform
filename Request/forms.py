from django import forms
from django.contrib.auth import get_user_model


class NewRequest(forms.Form):
    title = forms.CharField(max_length = 255)
    content = forms.CharField(widget=forms.Textarea(attrs = {'rows': 10, 'cols': 80}), required = False)
    User = get_user_model()
    agent = forms.ModelChoiceField(queryset = User.objects.all())
