from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="Firstname", max_length=40, required=True)
    last_name = forms.CharField(label="Lastname", max_length=40, required=True)
    username = forms.CharField(label="Telefon raqam", max_length=15, required=True)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'name': 'first_name',
            'id': 'first_name',
            'class': 'form-control',
            'placeholder': 'Firstname'
        })
        self.fields['last_name'].widget.attrs.update({
            'name': 'last_name',
            'id': 'last_name',
            'class': 'form-control',
            'placeholder': 'Lastname'
        })
        self.fields['username'].widget.attrs.update({
            'name': 'phone',
            'id': 'phoneNumber',
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Phone number'
        })
        self.fields['password1'].widget.attrs.update({
            'name': 'password1',
            'id': 'password1',
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'name': 'password2',
            'id': 'password2',
            'class': 'form-control mb-5',
            'placeholder': 'Password confirmation'
        })

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password1", "password2"]