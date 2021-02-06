from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model



class ProfileForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + \
            ('first_name', 'last_name', 'email', 'category') + ('image',)
            
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({
                'class': field + " form",
                'id': 'form-id', })





