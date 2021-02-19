from django.db import models
from user.models import User
from myApp.utils import uuid_name_upload_to

# Create your models here.


class Location(models.Model):

    # location
    address = models.TextField()  # 도로명 주소
    lat = models.FloatField(blank=True)
    lon = models.FloatField(blank=True)

    def __str__(self):
        return self.address


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
