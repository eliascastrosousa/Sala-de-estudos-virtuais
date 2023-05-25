from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ckeditor.widgets import CKEditorWidget


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class MessageForm(forms.Form):
    content = forms.CharField(
        widget=CKEditorWidget(
            attrs={
                "id": "messageInput",
                "type": "text",
                "name": "message",
                "class": "form-control",
                "aria-describedby": "button-addon2",
            }
        )
    )
