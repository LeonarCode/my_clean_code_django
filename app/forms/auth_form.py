from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from app.forms.styles import INPUT_CLASSES


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": INPUT_CLASSES,
            "placeholder": "you@example.com",
        }),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": INPUT_CLASSES,
            "placeholder": "Choose a username",
            "autofocus": True,
        })
        self.fields["password1"].widget.attrs.update({
            "class": INPUT_CLASSES,
            "placeholder": "Create a password",
        })
        self.fields["password2"].widget.attrs.update({
            "class": INPUT_CLASSES,
            "placeholder": "Confirm password",
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "class": INPUT_CLASSES,
            "placeholder": "Username",
            "autofocus": True,
        }),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "class": INPUT_CLASSES,
            "placeholder": "Password",
        }),
    )
