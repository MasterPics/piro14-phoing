from django.shortcuts import render, redirect
from .models import User, Portfolio, Post
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import HttpResponse
from .forms import *


def main_list(request):
    ctx = {}
    return render(request, 'myApp/main/main_list.html', context=ctx)

###################### profile section ######################


def profile_detail(request, pk):
    user = User.objects.get(pk=pk)
    choose = 'profile'
    ctx = {'user': user, 'choose': choose, }
    return render(request, 'myApp/profile/profile_detail.html', context=ctx)


# @login_required
def profile_delete(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "탈퇴되었습니다.")
        return redirect('myApp:main_list')
    else:
        ctx = {'user': user}
        return render(request, 'myApp/profile/profile_delete.html', context=ctx)


def profile_portfolio(request, pk):
    user = User.objects.get(pk=pk)
    portfolios = Portfolio.objects.filter(user=user)
    choose = 'portfolio'
    ctx = {'user': user, 'choose': choose, 'portfolios': portfolios}
    return render(request, 'myApp/profile/profile_portfolio.html', context=ctx)


def profile_update(request, profile_id):
    profile = get_object_or_404(User, pk=profile_id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            print("form.is_valid")

            profile = form.save()
            profile.image = request.FILES['image']
            return redirect('myApp:profile_detail', profile_id=profile_id)
    else:
        form = ProfileForm(instance=profile)
        ctx = {'form': form}
        return render(request, 'myApp/profile_update.html', ctx)


def profile_create(request):
    # if request.user.is_authenticated:
    #     return redirect('myApp:profile_detail')
        
    if request.method == 'POST':
        signup_form = ProfileForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = signup_form.save()
            user.image = request.FILES['image']
            return redirect('myApp:profile_detail', user.id)
    
    else:
        signup_form = ProfileForm()

    return render(request, 'myApp/profile_create.html', {'form':signup_form})