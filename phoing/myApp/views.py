from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import HttpResponse
from django.http import JsonResponse
import json
from django.views import View


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def main_list(request):
    ctx = {}
    return render(request, 'myApp/main/main_list.html', context=ctx)

###################### profile section ######################


def profile_detail(request, pk):
    user = User.objects.get_object_or_404(pk=pk)
    ctx = {'user': user, }
    return render(request, 'myApp/profile/profile_detail.html', context=ctx)


# @login_required
def profile_delete(request, pk):
    user = User.objects.get_object_or_404(pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "탈퇴되었습니다.")
        return redirect('myApp:main_list')
    else:
        ctx = {'user': user}
        return render(request, 'myApp/profile/profile_delete.html', context=ctx)


def profile_portfolio(request, pk):
    user = User.objects.get_object_or_404(pk=pk)
    portfolios = Portfolio.objects.filter(user=user)
    ctx = {'user': user, 'portfolios': portfolios}
    return render(request, 'myApp/profile/profile_portfolio.html', context=ctx)


def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            print("form.is_valid")

            user = form.save()
            user.image = request.FILES['image']
            return redirect('myApp:profile_detail', user.id)
    else:
        form = ProfileForm(instance=user)
        ctx = {'form': form}
        return render(request, 'myApp/profile/profile_update.html', ctx)


def profile_create(request):
    
    if request.method == 'POST':
        signup_form = ProfileForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = signup_form.save()
            user.image = request.FILES['image']
            return redirect('myApp:profile_detail', user.id)

    else:
        signup_form = ProfileForm()

    return render(request, 'myApp/profile/profile_create.html', {'form': signup_form})

###################### contact section ######################

def contact_list(request):
    contacts = Contact.objects.all().order_by("?")
    ctx = {'contacts' : contacts}
    return render(request, 'myApp/contact/contact_list.html', context=ctx)


def contact_detail(request, pk):
    contact = Contact.objects.get_object_or_404(pk=pk)
    ctx = {'contact': contact}
    return render(request, 'myApp/contact/contact_detail.html', context=ctx)


# @login_required
def contact_delete(request, pk):
    contact = Contact.objects.get_object_or_404(pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, "탈퇴되었습니다.")
        return redirect('myApp:contact_list')
    else:
        ctx = {'contact': contact}
        return render(request, 'myApp/contact/contact_delete.html', context=ctx)


# @login_required
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            print("form.is_valid")
            contact = form.save()
            contact.image = request.FILES['image']
            return redirect('myApp:contact_detail', contact.id)
    else:
        form = ContactForm(instance=contact)
        ctx = {'form': form}
        return render(request, 'myApp/contact/contact_update.html', ctx)


# @login_required
def contact_create(request):
    # if request.user.is_authenticated:
    #     return redirect('myApp:profile_detail')

    if request.method == 'POST':
        signup_form = ContactForm(request.POST, request.FILES)
        if signup_form.is_valid():
            contact = signup_form.save()
            contact.image = request.FILES['image']
            return redirect('myApp:contact_detail', user.id)

    else:
        signup_form = ContactForm()

    return render(request, 'myApp/contact/contact_create.html', {'form': signup_form})

'''
# @login_required
class ContactSave(View):
    template_name = 'contact/contact_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ContactSave, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        contacts = Contact.objects.all()
        ctx = {"contacts": contacts}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = json.loads(request.body)
        contact_id = data["id"]
        contact = Contact.objects.get(id=contact_id)
        save_users = contact.save_users.all()         
        if user.is_authenticated():
            if request.user in save_user:
                contact.save()

        return JsonResponse({'id': contact_id, 'save_users': contact.save_users})
'''