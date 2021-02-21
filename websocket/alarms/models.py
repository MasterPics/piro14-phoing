from django.db import models
# Create your models here.

class Alarm(models.Model):
    message=models.CharField(max_length=100)
    created_at= models.DateTimeField(auto_now_add=True, )