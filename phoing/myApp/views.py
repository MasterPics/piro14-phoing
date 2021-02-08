from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import HttpResponse
from .forms import *
from .models import *
import random
from django.http import JsonResponse
import json
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import login as auth_login


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def main_list(request):
    ctx = {}
    return render(request, 'myApp/main/main_list.html', context=ctx)

###################### profile section ######################


@login_required
def profile_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    ctx = {'user': user, }
    return render(request, 'myApp/profile/profile_detail.html', context=ctx)


@login_required
def profile_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "탈퇴되었습니다.")
        return redirect('myApp:main_list')
    else:
        ctx = {'user': user}
        return render(request, 'myApp/profile/profile_delete.html', context=ctx)


@login_required
def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            print("form.is_valid")

            user = form.save()
            if user.image:
                user.image = request.FILES['image']
            return redirect('myApp:profile_detail', user.id)
    else:
        form = ProfileForm(instance=user)
        ctx = {'form': form}
        return render(request, 'myApp/profile/profile_update.html', ctx)


def profile_create(request):
    # if request.user.is_authenticated:
    #     return redirect('myApp:profile_detail')

    if request.method == 'POST':
        signup_form = ProfileForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = signup_form.save()
            user.image = request.FILES['image']

            # automatic login
            auth_login(request, user,
                       backend='django.contrib.auth.backends.ModelBackend')

            return redirect('myApp:profile_detail', user.id)

    else:
        signup_form = ProfileForm()

    return render(request, 'myApp/profile/profile_create.html', {'form': signup_form})


@login_required
def profile_portfolio(request, pk):
    user = User.objects.get(pk=pk)
    portfolios = Portfolio.objects.filter(user=user)
    ctx = {'user': user, 'portfolios': portfolios}
    return render(request, 'myApp/profile/profile_portfolio.html', context=ctx)

###################### portfolio section ######################


def portfolio_list(request, filtering_type):
    random_ports = Portfolio.objects.order_by("?")

    photographer = User.objects.filter(category=User.CATEGORY_PHOTOGRAPHER)
    model = User.objects.filter(category=User.CATEGORY_MODEL)
    h_m = User.objects.filter(category=User.CATEGORY_HM)
    stylist = User.objects.filter(category=User.CATEGORY_STYLIST)
    other_use = User.objects.filter(category=User.CATEGORY_OTHER)

    # order by: random 으로 선택
    photographer = User.objects.filter(category=User.CATEGORY_PHOTOGRAPHER)
    photographer_ports = Portfolio.objects.filter(
        user=photographer).order_by("?")  # 단일 유저를 인자로 집어넣어야 함

    # 동일 기능
    Portfolio.objects.filter(
        user__type='Model'
    ).order_by("?")


    model_ports = Portfolio.objects.filter(user=model).order_by("?")
    h_m_ports = Portfolio.objects.filter(user=h_m).order_by("?")
    stylist_ports = Portfolio.objects.filter(user=stylist).order_by("?")
    other_use_ports = Portfolio.objects.filter(user=other_use).order_by("?")
    ctx = {'random_ports': random_ports,
           'photographer_ports': photographer_ports, 'model_ports': model, 'h_m_ports': h_m_ports, 'stylist_ports': stylist_ports, 'other_use_ports': other_use_ports}
    return render(request, 'myApp/portfolio/portfolio_list.html', context=ctx)


def portfolio_detail(request, pk):
    port = Portfolio.objects.get(pk=pk)
    tags = port.tags
    images = port.images
    owner = port.user
    owner_ports = Portfolio.objects.filter(user=owner)
    login_user = request.user
    ctx = {'port': port,
           'tags': tags, 'images': images,
           'owner': owner,
           'owner_ports': owner_ports,
           'login_user': login_user, }
    return render(request, 'myApp/portfolio/portfolio_detail.html', context=ctx)


def portfolio_delete(request, pk):
    port = Portfolio.objects.get(pk=pk)
    user = port.user
    if request.method == 'POST':
        port.delete()
        messages.success(request, "삭제되었습니다.")
        return redirect('myApp:profile_portfolio', user.id)
    else:
        ctx = {'port': port}
        return render(request, 'myApp/portfolio/portfolio_delete.html', context=ctx)


def portfolio_update(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save()
            portfolio.image = request.FILES['image']
            return redirect('myApp:portfolio_detail', portfolio.id)
    else:
        form = PortfolioForm()
        ctx = {'form': form}
        return render(request, 'myApp/portfolio/portfolio_update.html', ctx)


def portfolio_create(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES,)
        if form.is_valid():
            portfolio = form.save()
            portfolio.user = request.user
            portfolio.image = request.FILES['image']
            # TODO : save 다시
            return redirect('myApp:portfolio_detail', portfolio.id)

    else:
        form = PortfolioForm()
        ctx = {'form': form}

    return render(request, 'myApp/portfolio/portfolio_create.html', ctx)


class PortfolioLike(View):
    template_name = 'portfolio/portfolio_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PortfolioLike, self).dispatch(request, *args, **kwargs)

    def portfolio(self, request):

        data = json.loads(request.body)
        portfolio_id = data["id"]
        portfolio = Portfolio.objects.get(id=portfolio_id)
        portfolio.like = not portfolio.like
        portfolio.save()

        return JsonResponse({'id': portfolio_id, 'like': portfolio.like})


class PortfolioSave(View):
    template_name = 'portfolio/portfolio_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PortfolioSave, self).dispatch(request, *args, **kwargs)

    def portfolio(self, request):

        data = json.loads(request.body)
        portfolio_id = data["id"]
        portfolio = Portfolio.objects.get(id=portfolio_id)
        portfolio.save = not portfolio.save
        portfolio.save()

        return JsonResponse({'id': portfolio_id, 'save': portfolio.save})


###################### contact section ######################

def contact_list(request):
    contacts = Contact.objects.all().order_by("?")
    ctx = {'contacts': contacts}
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
        contact_form = ContactForm(request.POST, request.FILES)
        if contact_form.is_valid():
            contact = contact_form.save()
            contact.image = request.FILES['image']
            return redirect('myApp:contact_detail', user.id)

    else:
        contact_form = ContactForm()

    return render(request, 'myApp/contact/contact_create.html', {'form': contact_form})


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
