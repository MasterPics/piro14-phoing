from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import uuid_name_upload_to
# Create your models here.


class User(AbstractUser):
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
    category = models.CharField(max_length=20, choices=CATEGORY)
    image = models.ImageField(
        upload_to=uuid_name_upload_to, blank=True, default='user.png')


class Post(models.Model):
    user = models.ForeignKey(
        to=User, related_name="posts", on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=uuid_name_upload_to)
    title = models.CharField(max_length=30)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    save_users = models.ManyToManyField(
        to=User, related_name='save_users', blank=True)

    def __str__(self):
        return self.title


class Contact(Post):  # also Collaborate
    file_attach = models.FileField()
    location = models.TextField()
    pay = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_closed = models.BooleanField(default=False)


class Portfolio(Post):
    like_users = models.ManyToManyField(
        to=User, related_name='like_users', blank=True)
    view_count = models.PositiveIntegerField(default=0)


class Comment(models.Model):
    post = models.ForeignKey(
        to=Post, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    post = models.ManyToManyField(to=Post, related_name="tags")
    tag = models.CharField(max_length=30)


class Image(models.Model):
    post = models.ForeignKey(
        to=Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=uuid_name_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
