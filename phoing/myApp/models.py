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
import json
import datetime

from place.models import Location
from django_mysql.models import ListCharField
from django.utils import timezone



class Tag(models.Model):
    tag = models.CharField(max_length=30)
    save_users = models.ManyToManyField(
        to=User, related_name='tag_save_users', blank=True)
    like_users = models.ManyToManyField(
        to=User, related_name='tag_like_users', blank=True)

    @classmethod
    def add_tags(selt, tag_str):
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
    tag_str = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField(Tag, related_name='contacts', blank=True)

    # specific field
    file_attach = models.FileField()
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, default=None, blank=True)
    pay = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_closed = models.BooleanField(default=False)
    tag_str = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField(Tag, related_name='contacts', blank=True)

    def to_json(self):
        return {
            "pk": self.pk,
            "title": self.title,
            "pay": self.pay,
            "start_date": self.start_date.strftime('%Y-%m-%d'),
            "end_date": self.end_date.strftime('%Y-%m-%d'),
            "address": self.location.address,
            "lat": self.location.lat,
            "lon": self.location.lon,
        }

    def classname(self):
        return self.__class__.__name__


class CollaborationWithBrand(models.Model):
    # common field
    user = models.ForeignKey(
        to=User, related_name="with_brands", on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=uuid_name_upload_to)
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    save_users = models.ManyToManyField(
        to=User, related_name='with_brand_save_users', blank=True)
    desc = models.TextField()
    tag_str = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField(Tag, related_name='with_brand', blank=True)

    # specific field
    file_attach = models.FileField()
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, default=None, blank=True)
    pay = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_closed = models.BooleanField(default=False)

    def to_json(self):
        return {
            "pk": self.pk,
            "title": self.title,
            "pay": self.pay,
            "start_date": self.start_date.strftime('%Y-%m-%d'),
            "end_date": self.end_date.strftime('%Y-%m-%d'),
            "address": self.location.address,
            "lat": self.location.lat,
            "lon": self.location.lon,
        }


class CollaborationWithArtist(models.Model):
    # common field
    user = models.ForeignKey(
        to=User, related_name="with_artists", on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=uuid_name_upload_to)
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    save_users = models.ManyToManyField(
        to=User, related_name='with_artist_save_users', blank=True)
    desc = models.TextField()
    tag_str = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField(Tag, related_name='with_artists', blank=True)

    # specific field
    file_attach = models.FileField()
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, default=None, blank=True)
    pay = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_closed = models.BooleanField(default=False)

    def to_json(self):
        return {
            "pk": self.pk,
            "title": self.title,
            "pay": self.pay,
            "start_date": self.start_date.strftime('%Y-%m-%d'),
            "end_date": self.end_date.strftime('%Y-%m-%d'),
            "address": self.location.address,
            "lat": self.location.lat,
            "lon": self.location.lon,
        }


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
    view_count = models.PositiveIntegerField(default=0)
    like_users = models.ManyToManyField(
        to=User, related_name='portfolio_like_users', blank=True)
    tag_str = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField(Tag, related_name='portfolios', blank=True)

    def classname(self):
        return self.__class__.__name__


class Reference(models.Model):
    thumbnail = models.ImageField(upload_to=uuid_name_upload_to)
    save_users = models.ManyToManyField(
        to=User, related_name='reference_save_users', blank=True)
    like_users = models.ManyToManyField(
        to=User, related_name='reference_like_users', blank=True)
    desc = models.TextField()
    image_url = ListCharField(base_field=models.CharField(
        max_length=100), max_length=60000)
    tag_str = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField(Tag, related_name='references', blank=True)


class Comment(models.Model):
    contact = models.ForeignKey(
        to=Contact, null=True, blank=True, related_name='contact_comments', on_delete=models.CASCADE)
    portfolio = models.ForeignKey(
        to=Portfolio, null=True, blank=True, related_name='portfolio_comments', on_delete=models.CASCADE)
    with_brand = models.ForeignKey(
        to=CollaborationWithBrand, null=True, blank=True, related_name='with_brand_comments', on_delete=models.CASCADE)
    with_artist = models.ForeignKey(
        to=CollaborationWithBrand, null=True, blank=True, related_name='with_artist_comments', on_delete=models.CASCADE)

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Images(models.Model):
    contact = models.ForeignKey(
        to=Contact, null=True, blank=True, related_name='contact_images', on_delete=models.CASCADE)
    portfolio = models.ForeignKey(
        to=Portfolio, null=True, blank=True, related_name='portfolio_images', on_delete=models.CASCADE)
    with_brand = models.ForeignKey(
        to=CollaborationWithBrand, null=True, blank=True, related_name='with_brand_images', on_delete=models.CASCADE)
    with_artist = models.ForeignKey(
        to=CollaborationWithBrand, null=True, blank=True, related_name='with_artist_images', on_delete=models.CASCADE)
    reference = models.ForeignKey(
        to=Reference, null=True, blank=True, related_name='reference_images', on_delete=models.CASCADE)

    image = models.ImageField(
        upload_to=uuid_name_upload_to, blank=True,null=True, verbose_name='Image')
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


class Place(models.Model):
    # common field
    user = models.ForeignKey(
        to=User, related_name="posts", on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=uuid_name_upload_to)
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    save_users = models.ManyToManyField(
        to=User, related_name='save_users', blank=True)
    desc = models.TextField()

    # specific field
    like_users = models.ManyToManyField(
        to=User, related_name='like_users', blank=True)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, default=None, blank=True)
    pay = models.PositiveIntegerField()
    tag_str = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField(Tag, related_name='places', blank=True)

    def to_json(self):
        return {
            'user': self.user,
            'thumbnail': self.thumbnail.url,
            'title': self.title,
            'location': self.location,
            'lat': self.location.lat,
            'lon': self.location.lon,
            'pay': self.location.pay,
            'tag_str': ' '.join([tag.tag for tag in tags.all()])
        }

class ViewCount(models.Model):
    ip=models.CharField(max_length=15, default=None, null=True)
    post=models.ForeignKey(Portfolio, default=None, null=True, related_name='view_counts', on_delete=models.CASCADE)
    date=models.DateField(default=timezone.now(), null=True, blank=True)
