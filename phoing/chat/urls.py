# chat/urls.py
from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/home/', views.chat_home, name='chat_home'),
    path('pending/', views.chat_add_pendings, name='chat_add_pendings'),
    path('member/', views.chat_add_members, name='chat_add_members'),
    path('reject/', views.chat_add_rejected, name='chat_add_rejected'),
    path('<str:room_name>/', views.chat_room, name='room'),
   
]