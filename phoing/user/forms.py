from django import forms
from allauth.socialaccount.forms import SignupForm
from allauth.account.forms import SignupForm
from myApp.utils import uuid_name_upload_to
from .models import User
from django.core.exceptions import ValidationError

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


# class MyCustomSignupForm(SignupForm):

#     # access to current user by self.current_user

#     username = forms.CharField(max_length=20, required=False)
#     first_name = forms.CharField(max_length=20, required=False)
#     last_name = forms.CharField(max_length=20, required=False)
#     email = forms.EmailField(help_text='A valid email address, please.')
#     category = forms.ChoiceField(choices=CATEGORY)
#     image = forms.ImageField(required=False)
#     desc = forms.CharField(widget=forms.Textarea, required=False)

#     class Meta:
#         model = User

#     def save(self, request):
#         # Ensure you call the parent class's save.
#         # .save() returns a User object.
#         user = super(MyCustomSignupForm, self).save(request)
#         # user.username = self.cleaned_data['username']
#         user.email = self.cleaned_data['email']
#         user.image = self.cleaned_data['image']
#         user.desc = self.cleaned_data['desc']
#         user.save()

#         # Add your own processing here.

#         # You must return the original result.
#         return user


# class MyCustomSocialSignupForm(SignupForm):

#     def __init__(self, sociallogin=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     username = forms.CharField(max_length=20, required=False)
#     first_name = forms.CharField(max_length=20, required=False)
#     last_name = forms.CharField(max_length=20, required=False)
#     category = forms.ChoiceField(choices=CATEGORY)
#     desc = forms.CharField(widget=forms.Textarea, required=False)

#     class Meta:
#         model = User

#     def save(self, request):

#         # Ensure you call the parent class's save.
#         # .save() returns a User object.
#         user = super(MyCustomSocialSignupForm, self).save(request)

#         # Add your own processing here.

#         # You must return the original result.
#         return user

# class SignUpForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ("username", "email", "category", "image","desc", "password",)

# class UpdateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ("username", "email", "category", "image","desc",)

# class SignUpForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ("username", "email", "category", "image","desc")
#         widgets = {
#             "username" : forms.TextInput(
#                 attrs={
#                 "placeholder": "Enter username", 
#                 "class":"signup-username signup-form"
#                 }
#             ),
#             "email" : forms.TextInput(
#                 attrs={
#                     "placeholder": "Enter email", 
#                     "class":"signup-email signup-form"
#                     }
#             ),
#             # "category" : forms.ChoiceField(
#             #     attrs={
#             #         "class":"signup-category signup-form"
#             #         }
#             # ),
#             "desc" : forms.Textarea(attrs={"placeholder": "Enter description", "class":"signup-desc signup-form"}),
#         }

#     image = forms.ImageField()
#     category = forms.ChoiceField(choices=User.CATEGORY)

#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={"placeholder": "Password"})
#     )
#     password1 = forms.CharField(
#         widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
#     )

#     code = 'invalid'

#     required = {
#             'username': True,
#             'email': True,
#             'category': True,
#             'img': True,
#         }

#     def clean_password1(self):
#         password = self.cleaned_data.get("password")
#         password1 = self.cleaned_data.get("password1")
#         if password != password1:
#             raise forms.ValidationError("Password confirmation does not match")
#         else:
#             return password


#     def save(self, *args, **kwargs):
#         user = super().save(commit=False)
#         password = self.cleaned_data.get("password")
#         user.set_password(password)
#         user.save()



# class LoginForm(forms.Form):
#     username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "class": "login-username login-form"}))
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "login-password login-form"})
#     )

#     def clean(self):
#         username = self.cleaned_data.get("username")
#         password = self.cleaned_data.get("password")
#         try:
#             user = User.objects.get(username)
#             # if user.email_verified == False:
#             #     self.add_error("email", forms.ValidationError("이메일 인증을 완료해야만 로그인이 가능합니다."))
#             #     raise forms.ValidationError("이메일 인증을 완료해야만 로그인이 가능합니다.")
            
#             if user.check_password(password):
#                 return self.cleaned_data
#             else:
#                 self.add_error("password", forms.ValidationError("Password is wrong"))
#                 raise forms.ValidationError("Password is wrong")
#         except models.User.DoesNotExist:
#             self.add_error("email", forms.ValidationError("User does not exist"))
#             raise forms.ValidationError("User does not exist")


class SignUpForm(forms.ModelForm):

    pw1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control form-pw1', 'placeholder': '비밀번호'}))
    pw2 = forms.CharField(label='비밀번호 재입력', widget=forms.PasswordInput(attrs={'class': 'form-control form-pw2', 'placeholder': '비밀번호 재입력'}))
    
    
    def clean(self):
        pw1 = self.cleaned_data['pw1']
        pw2 = self.cleaned_data['pw2']

        if pw1 == pw2:
            self.cleaned_data['pw'] = pw1
        else:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("동일한 아이디가 이미 존재합니다. ")
        
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("동일한 이메일로 가입된 계정이 존재합니다.")

        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username','email', 'image','category','desc')
        widgets = {
            'category': forms.Select(choices=CATEGORY,attrs={'class': 'form-control category'}),
        }
        # help_texts = {'phone_number': "ex) 01X-XXX-XXXX",}
        # widgets = {
        #     'phone_number':forms.TextInput(attrs={'class':'form-control','placeholder':'전화번호'}),
        # }

class UpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','email', 'image','category','desc')
        widgets = {
            'category': forms.Select(choices=CATEGORY,attrs={'class': 'form-control category'}),
            'email': forms.TextInput(attrs={'disabled': True}),
        }
        

    def clean(self):

        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError("동일한 아이디가 이미 존재합니다. ")

        return self.cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label=아이디, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '아이디'}))
    pw = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호'}))



# class NewpwForm(forms.Form):
#     current_pw = forms.CharField(label='현재 비밀번호', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': '현재 비밀번호'}))
#     new_pw1 = forms.CharField(label='새 비밀번호', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': '새 비밀번호'}))
#     new_pw2 = forms.CharField(label='비밀번호 재입력', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': '비밀번호 재입력'}))

# class ChangepwForm(forms.Form):
#     userid = forms.CharField(label='아이디를 입력하세요.', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '아이디를 입력하세요.'}))
#     email = forms.EmailField(label='등록한 이메일을 입력하세요.', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': '등록한 이메일을 입력하세요.'}))

# class CheckForm(forms.Form):
#     username = forms.CharField(label='닉네임을 입력하세요.', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '닉네임을 입력하세요.'}))
#     pw1 = forms.CharField(label='비밀번호를 입력하세요.', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': '비밀번호를 입력하세요.'}))
#     pw2 = forms.CharField(label='비밀번호를 확인해주세요.', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': '비밀번호를 확인해주세요.'}))

