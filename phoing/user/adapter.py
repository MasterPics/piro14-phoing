from __future__ import absolute_import

from myApp.utils import uuid_name_upload_to, save_image_from_url
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from allauth.account import app_settings as account_settings
from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.account.app_settings import EmailVerificationMethod
from allauth.account.models import EmailAddress
from allauth.account.utils import user_email, user_field, user_username
from allauth.utils import (
    deserialize_instance,
    email_address_exists,
    import_attribute,
    serialize_instance,
    valid_email_or_none,
)
from allauth.socialaccount import app_settings

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.dispatch import receiver
from allauth.account.signals import user_signed_up


class MyCustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    @receiver(user_signed_up)
    def populate_profile(sociallogin, user, **kwargs):

        if sociallogin.account.provider == 'naver':
            user_data = user.socialaccount_set.filter(provider='naver')[
                0].extra_data
            print(user_data)
            picture_url = user_data["profile_image"]
            print(picture_url)
            username = user_data["nickname"]
            # first_name = user_data['first_name']

        if sociallogin.account.provider == 'kakao':
            user_data = user.socialaccount_set.filter(provider='kakao')[
                0].extra_data
            picture_url = user_data["properties"]["profile_image"]
            username = user_data["properties"]["nickname"]

        if sociallogin.account.provider == 'google':
            user_data = user.socialaccount_set.filter(
                provider='google')[0].extra_data
            picture_url = user_data["picture"]
            username = user_data["name"]

        user.username = username
        save_image_from_url(user, picture_url)
        user.save()

    # @receiver(user_signed_up)
    # def populate_profile(user, **kwargs):
    #     print("Local")
    #     pass
