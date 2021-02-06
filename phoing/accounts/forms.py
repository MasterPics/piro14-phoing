from django.contrib.auth.forms import AuthenticationForm

from django import forms


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    # username = forms.EmailField(widget=forms.TextInput(
    #     attrs={'class': 'form-control email ', 'placeholder': 'email address', 'id': 'hello'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control username',
               'placeholder': 'username',
               'id': 'username login-username',
               }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control password',
            'placeholder': 'password',
            'id': 'password login-password',
        }
    ))



