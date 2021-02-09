from django import forms
from allauth.socialaccount.forms import SignupForm
from allauth.account.forms import SignupForm
from myApp.utils import uuid_name_upload_to
from .models import User

CATEGORY_PHOTOGRAPHER = 'photographer'
CATEGORY_MODEL = 'model'
CATEGORY_HM = 'HairMakeup'
CATEGORY_STYLIST = 'stylist'
CATEGORY_OTHERS = 'otheruse'

CATEGORY = (('', '---------'),
            ('photographer', CATEGORY_PHOTOGRAPHER),
            ('model', CATEGORY_MODEL),
            ('HairMakeup', CATEGORY_HM),
            ('stylist', CATEGORY_STYLIST),
            ('otheruse', CATEGORY_OTHERS),
            )


class MyCustomSignupForm(SignupForm):

    # access to current user by self.current_user

    username = forms.CharField(max_length=20, required=False)
    first_name = forms.CharField(max_length=20, required=False)
    last_name = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(help_text='A valid email address, please.')
    category = forms.ChoiceField(choices=CATEGORY)
    image = forms.ImageField(required=False)
    desc = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)
        # user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.image = self.cleaned_data['image']
        user.desc = self.cleaned_data['desc']
        user.save()

        # Add your own processing here.

        # You must return the original result.
        return user


class MyCustomSocialSignupForm(SignupForm):

    def __init__(self, sociallogin=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.CharField(max_length=20, required=False)
    first_name = forms.CharField(max_length=20, required=False)
    last_name = forms.CharField(max_length=20, required=False)
    category = forms.ChoiceField(choices=CATEGORY)
    desc = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSocialSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user
