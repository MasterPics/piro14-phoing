# chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

@login_required
def chat_home(request, pk):

    user = User.objects.get(pk=pk)
    print(Group.objects.get(pk=1))
    ctx = {

    }
    return render(request, 'chat/chat_home.html', context=ctx)