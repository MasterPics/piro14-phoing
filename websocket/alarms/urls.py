from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('ShareMe', views.ShareMe.as_view()),
    path('Alarm', views.Alarm.as_view()),
]