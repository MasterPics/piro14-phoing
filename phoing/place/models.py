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
