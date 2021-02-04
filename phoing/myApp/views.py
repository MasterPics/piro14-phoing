from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib import messages 
from .forms import *

# Create your views here.

# def profile_create(request):

#     ctx = {}
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES)
#         print(form.errors)

#         if form.is_valid():
#             profile = form.save()
#             return redirect('myApp:profile_detail', profile.id)


#     else:
#         form = ProfileForm()
#         ctx = {'form': form}
#         return render(request, template_name='myApp/profile_create.html', context=ctx)


def profile_create(request):
    # if request.user.is_authenticated:
    #     return redirect('myApp:profile_detail')
        
    if request.method == 'POST':
        signup_form = ProfileForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = signup_form.save()
            return redirect('myApp:profile_detail', user.id)
    
    else:
        signup_form = ProfileForm()

    return render(request, 'myApp/profile_create.html', {'form':signup_form})


    