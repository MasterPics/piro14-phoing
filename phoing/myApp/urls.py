from django.urls import path
from .views import *

app_name = 'myApp'

urlpatterns = [
    path('profile/create', profile_create, name='profile_create'),
    
]
