from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth import login as auth_login
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from django.forms import modelformset_factory

# from event.models import Evente

# from login.forms import MemberForm, CreatorForm
# from login.models import Creator, Member

from .models import User
from .forms import SignUpForm, LoginForm, UpdateForm

from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


app_name = 'login'

def login_main(request):

    ctx = {
        
    }

    return render(request, 'login/login_main.html', context=ctx)

def signup_main(request):

    ctx = {
        
    }

    return render(request, 'login/signup_main.html', context=ctx)

def login_form(request):

    ctx = {
        
    }

    return render(request, 'login/login_form.html', context=ctx)


def signup_form(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return()



    ctx = {
        
    }

    return render(request, 'login/signup_form.html', context=ctx)

def signup(request):
    if request.method == "POST":
        user_form = CreateUserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)  # 로그인 처리
            return redirect('accounts:signup_profile')

    elif request.method == "GET":
        user_form = CreateUserForm()

    return render(request, 'accounts/signup.html', {
        'user_form': user_form,
    })

def signup_form_social(request):

    ctx = {
        
    }

    return render(request, 'login/signup_form_social.html', context=ctx)


@login_required
def profile_update(request, pk):

    ctx = {
        
    }

    return render(request, 'login/profile_update.html', context=ctx)


@login_required
def password_update(request, pk):

    ctx = {

    }

    return render(request, 'login/password_update.html', context=ctx)




