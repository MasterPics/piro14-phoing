# chat/urls.py
from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('<int:pk>/home/', views.chat_home, name='chat_home'),
    path('add/', views.chat_add_pendings, name='chat_add_pendings')
]