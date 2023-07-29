from django import forms
from django.core.validators import RegexValidator

from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30, validators=[RegexValidator(r"^[a-zA-Z0-9_]+$")]
    )
    password = forms.CharField(
        max_length=30, validators=[RegexValidator(r"^[a-zA-Z0-9_]+$")]
    )


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        max_length=30, validators=[RegexValidator(r"^[a-zA-Z0-9_]+$")]
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
