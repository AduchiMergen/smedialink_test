from django import forms

from partymaker.models import User


class AuthForm(forms.ModelForm):
    class Meta:
        model = User
