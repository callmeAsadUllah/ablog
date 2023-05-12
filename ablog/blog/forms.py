from django import forms
from django.forms import (
    Form,
    ModelForm
)
# from django.contrib.auth.models import User


from .models import (
    PostModel,
    CommentModel
)


class EmailPostForm(Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)


class CommentForm(ModelForm):
    class Meta:
        model = CommentModel
        fields = [
            'name',
            'email',
            'body'
        ]