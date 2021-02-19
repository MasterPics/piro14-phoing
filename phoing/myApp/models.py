from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .utils import uuid_name_upload_to, save_image_from_url
from django.utils.translation import ugettext_lazy as _

from django.dispatch import receiver
from allauth.account.signals import user_signed_up
import urllib

from django.shortcuts import redirect
from user.models import User
import re

from django_mysql.models import ListCharField


class Tag(models.Model):
    tag = models.CharField(max_length=30)

    @classmethod
    def add_tags(self, tag_str):
        # NOTE: self.desc 말고 TAG FIELD 따로 만들까?
        tags = re.findall(r'#(\w+)\b', tag_str)
        tag_lst = []

        for t in tags:
            tag, tag_created = Tag.objects.get_or_create(tag=t)
            tag_lst.append(tag)

        return tag_lst

    def __str__(self):
        return self.tag


class Contact(models.Model):
    # common field
    user = models.ForeignKey(
        to=User, related_name="contacts", on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=uuid_name_upload_to)
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    save_users = models.ManyToManyField(
        to=User, related_name='contact_save_users', blank=True)
    desc = models.TextField()

    # specific field
    file_attach = models.FileField()
    location = models.TextField()
    pay = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_closed = models.BooleanField(default=False)


class Portfolio(models.Model):
    # common field
    user = models.ForeignKey(
        to=User, related_name="portfolios", on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=uuid_name_upload_to)
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    save_users = models.ManyToManyField(
        to=User, related_name='portfolio_save_users', blank=True)
    desc = models.TextField()

    # specific field
    like_users = models.ManyToManyField(
        to=User, related_name='portfolio_like_users', blank=True)
    view_count = models.PositiveIntegerField(default=0)
    tag_str = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField(Tag, related_name='portfolios', blank=True)


class Reference(models.Model):
    thumbnail = models.ImageField(upload_to=uuid_name_upload_to)
    tag = models.OneToOneField(
        to=Tag, related_name='reference', on_delete=models.CASCADE)
    save_users = models.ManyToManyField(
        to=User, related_name='reference_save_users', blank=True)
    like_users = models.ManyToManyField(
        to=User, related_name='reference_like_users', blank=True)
    desc = models.TextField()
    image_url = ListCharField(base_field=models.CharField(
        max_length=100), max_length=60000)


class Comment(models.Model):
    contact = models.ForeignKey(
        to=Contact, null=True, blank=True, related_name='contact_comments', on_delete=models.CASCADE)
    portfolio = models.ForeignKey(
        to=Portfolio, null=True, blank=True, related_name='portfolio_comments', on_delete=models.CASCADE)

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Image(models.Model):
    contact = models.ForeignKey(
        to=Contact, null=True, blank=True, related_name='contact_images', on_delete=models.CASCADE)
    portfolio = models.ForeignKey(
        to=Portfolio, null=True, blank=True, related_name='portfolio_images', on_delete=models.CASCADE)
    reference = models.ForeignKey(
        to=Reference, null=True, blank=True, related_name='reference_images', on_delete=models.CASCADE)

    image = models.ImageField(upload_to=uuid_name_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# class Post(models.Model):
#     user = models.ForeignKey(
#         to=User, related_name="posts", on_delete=models.CASCADE)
#     thumbnail = models.ImageField(upload_to=uuid_name_upload_to)
#     title = models.CharField(max_length=30)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     save_users = models.ManyToManyField(
#         to=User, related_name='save_users', blank=True)
#     desc = models.TextField()

#     def __str__(self):
#         return self.title


# class Place(models.Model):
#     #common field
#     user = models.ForeignKey(
#         to=User, related_name="posts", on_delete=models.CASCADE)
#     thumbnail = models.ImageField(upload_to=uuid_name_upload_to)
#     title = models.CharField(max_length=30)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     save_users = models.ManyToManyField(
#         to=User, related_name='save_users', blank=True)
#     desc = models.TextField()

#     #specific field
#     like_users = models.ManyToManyField(
#         to=User, related_name='like_users', blank=True)
#     location = models.TextField()
#     pay = models.PositiveIntegerField()
