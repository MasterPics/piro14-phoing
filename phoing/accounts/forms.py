from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

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


class MySocialCustomSignupForm(forms.Form):

    CATEGORY_PHOTOGRAPHER = 'photographer'
    CATEGORY_MODEL = 'model'
    CATEGORY_HM = 'HairMakeup'
    CATEGORY_STYLIST = 'stylist'
    CATEGORY_OTHER = 'other use'

    CATEGORY = (
        ('photographer', CATEGORY_PHOTOGRAPHER),
        ('model', CATEGORY_MODEL),
        ('HairMakeup', CATEGORY_HM),
        ('stylist', CATEGORY_STYLIST),
        ('other use', CATEGORY_OTHER),
    )

    category = forms.ChoiceField(choices=CATEGORY)

    def signup(self, request, user):
        user.category = self.changed_data['category']
        user.save()
