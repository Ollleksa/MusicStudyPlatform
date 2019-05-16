from django import forms


class NewLesson(forms.Form):
    title = forms.CharField(max_length = 255)
    content = forms.CharField(widget=forms.Textarea(attrs = {'rows': 10, 'cols': 80}))
