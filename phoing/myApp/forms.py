from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class ProfileForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'category') +('image',)
        
    







