from django.db import models
from myApp.utils import uuid_name_upload_to, save_image_from_url
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from django.dispatch import receiver
from allauth.account.signals import user_signed_up
import urllib


# Create your models here.

from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    CATEGORY_PHOTOGRAPHER = 'photographer'
    CATEGORY_MODEL = 'model'
    CATEGORY_HM = 'HairMakeup'
    CATEGORY_STYLIST = 'stylist'
    CATEGORY_OTHERS = 'otheruse'

    CATEGORY = (
        ('photographer', CATEGORY_PHOTOGRAPHER),
        ('model', CATEGORY_MODEL),
        ('HairMakeup', CATEGORY_HM),
        ('stylist', CATEGORY_STYLIST),
        ('otheruse', CATEGORY_OTHERS),
    )

    username = models.CharField(max_length=20, blank=True, unique=False)
    email = models.EmailField('email address', unique=True)
    category = models.CharField(
        max_length=20, choices=CATEGORY)
    image = models.ImageField(
        upload_to=uuid_name_upload_to, blank=True)
    desc = models.TextField(blank=True)
    # objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return self.username


# @receiver(user_signed_up)
# def populate_profile(sociallogin, user, **kwargs):

#     if sociallogin.account.provider == 'naver':
#         user_data = user.socialaccount_set.filter(provider='naver')[
#             0].extra_data
#         picture_url = user_data["profile_image"]
#         # username = user_data["nickname"]
#         # first_name = user_data['first_name']

#     if sociallogin.account.provider == 'kakao':
#         user_data = user.socialaccount_set.filter(provider='kakao')[
#             0].extra_data
#         picture_url = user_data["properties"]["profile_image"]
#         # username = user_data["properties"]["nickname"]

#     if sociallogin.account.provider == 'google':
#         user_data = user.socialaccount_set.filter(
#             provider='google')[0].extra_data
#         picture_url = user_data["picture"]
#         # username = user_data["name"]

#     # user.username = username
#     save_image_from_url(user, picture_url)
#     user.save()
