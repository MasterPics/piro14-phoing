# chat/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import *
from django.views.decorators.csrf import csrf_exempt
from myApp.models import *
from django.http import JsonResponse

DEFAULT = 0
PENDING = 1
MEMBER = 2
REJECTED = 3

User = get_user_model()

def index(request):
    return render(request, 'chat/index.html', {})

def chat_room(request, room_name):
    return render(request, 'chat/chat_room.html', {
        'room_name': room_name
    })

@login_required
def chat_home(request, pk):

    user = User.objects.get(pk=pk)

    ctx = {

    }
    return render(request, 'chat/chat_home.html', context=ctx)


@csrf_exempt
def chat_add_members(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        contact_pk = data["contact_pk"]
        request_user_pk = data["request_user_pk"]
        contact = get_object_or_404(Contact, pk=contact_pk)
        request_user = get_object_or_404(User, pk=request_user_pk)
        contact.group.pendings.remove(request_user)
        contact.group.members.add(request_user)
        return JsonResponse(
            {
                'contact_pk': contact_pk,
                'member_pk': request_user_pk,
                'member_username': request_user.username,
                'member_category': request_user.category,
            }
        )

    

@csrf_exempt
def chat_add_pendings(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        contact_pk = data["contact_pk"]
        request_user_pk = data["request_user_pk"]
        contact = get_object_or_404(Contact, pk=contact_pk)
        request_user = get_object_or_404(User, pk=request_user_pk)
        contact.group.pendings.add(request_user)
        return JsonResponse(
            {
                'contact_pk' : contact_pk,
            }
        )


@csrf_exempt
def chat_add_rejected(request):
    print("Here")
    if request.method == 'POST':
        data = json.loads(request.body)
        contact_pk = data["contact_pk"]
        request_user_pk = data["request_user_pk"]
        contact = get_object_or_404(Contact, pk=contact_pk)
        request_user = get_object_or_404(User, pk=request_user_pk)
        contact.group.pendings.remove(request_user)
        contact.group.rejected.add(request_user)
        return JsonResponse(
            {
                'contact_pk' : contact_pk,
                'member_pk' : request_user_pk,
            }
        )

        


    