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


from django.db.models import Count, Q



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
            # print("form.is_valid")

            # user = form.save()
            # if user.image:
            #     user.image = request.FILES.get('image')
            # return redirect('myApp:profile_detail', user.id)
            user.image = request.FILES.get('image')
            user = form.save()
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


def profile_detail_other(request, pk):
    user = User.objects.get(pk=pk)
    portfolios = Portfolio.objects.filter(user=user)
    ctx = {'user': user, 'portfolios': portfolios}
    return render(request, 'myApp/profile/profile_detail_other.html', context=ctx)

###################### portfolio section ######################


def portfolio_list(request, category):
    ports = Portfolio.objects.all()

    # category 분류 # order by: random 으로 선택
    if category == 'all':
        ports = ports.order_by("?")
    else:
        if category == User.CATEGORY_PHOTOGRAPHER:
            ports = ports.objects.values('user').filter(
                category=CATEGORY_PHOTOGRAPHER).order_by("?")
        elif category == User.CATEGORY_MODEL:
            ports = ports.order_by("?")
        elif category == User.CATEGORY_HM:
            ports = ports.order_by("?")
        elif category == User.CATEGORY_STYLIST:
            ports = ports.order_by("?")
        elif category == User.CATEGORY_OTHER:
            ports = ports.order_by("?")

    context = {'ports': ports, }
    return render(request, 'myApp/portfolio/portfolio_list.html', context=context)


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
    
    if request.method == 'POST':
        pass
    else:
        contacts = Contact.objects.all()

        
        category = request.GET.get('category', 'all')
        search = request.GET.get('search', '')  # 검색어
        sort = request.GET.get('sort', 'recent')  # 정렬기준
        
        #category 분류
        if category != 'all':
            if category == User.CATEGORY_PHOTOGRAPHER:
                contacts = contacts.filter(Q(user__category=User.CATEGORY_PHOTOGRAPHER)
                ).distinct().order_by("?")
            elif category == User.CATEGORY_MODEL:
                contacts = contacts.filter(Q(user__category=User.CATEGORY_MODEL)
                ).distinct().order_by("?")
            elif category == User.CATEGORY_HM:
                contacts = contacts.filter(Q(user__category=User.CATEGORY_HM)
                ).distinct().order_by("?")
            elif category == User.CATEGORY_STYLIST:
                contacts = contacts.filter(Q(user__category=User.CATEGORY_STYLIST)
                ).distinct().order_by("?")
            elif category == User.CATEGORY_OTHER:
                contacts = contacts.filter(Q(user__category=User.CATEGORY_OTHER)
                ).distinct().order_by("?")
                #카테고리가 없는 유저들이 other use는 아님. 따로 있다!
        
        # 정렬
        if sort == 'save':
            contacts = contacts.annotate(num_save=Count('save_users')).order_by('-num_save', '-created_at')
        elif sort == 'pay':  
            contacts = contacts.order_by('-pay', '-created_at')
        elif sort == 'recent':
            contacts = contacts.order_by('-created_at')
        
        # 검색
        if search:
            contacts = contacts.filter(
                Q(title__icontains=search) |  # 제목검색
                Q(desc__icontains=search) |  # 내용검색
                Q(user__username__icontains=search)  # 질문 글쓴이검색
            ).distinct()

        context = {'contacts': contacts, 'sort':sort, 'category':category, 'search':search,}
        return render(request, 'myApp/contact/contact_list.html', context = context)


def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    login_user = request.user
    owner_user = contact.user
    ctx = {
        'contact': contact,
        'login_user': login_user,
        'owner_user': owner_user,
    }
    return render(request, 'myApp/contact/contact_detail.html', context=ctx)


@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, "탈퇴되었습니다.")
        return redirect('myApp:contact_list')
    else:
        ctx = {'contact': contact}
        return render(request, 'myApp/contact/contact_delete.html', context=ctx)


@login_required
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            print("form.is_valid")
            contact.image = request.FILES.get('image')
            contact = form.save()
            return redirect('myApp:contact_detail', contact.id)
    else:
        form = ContactForm(instance=contact)
        ctx = {'form': form}
        return render(request, 'myApp/contact/contact_update.html', ctx)


@login_required
def contact_create(request):
    # if request.user.is_authenticated:
    #     return redirect('myApp:profile_detail')

    if request.method == 'POST':
        contact_form = ContactForm(request.POST, request.FILES)
        if contact_form.is_valid():
            print('here')
            contact = contact_form.save(commit=False)
            contact.user = request.user
            contact.is_closed = False
            contact.save()
            contact.image = request.FILES.get('image')
            return redirect('myApp:contact_detail', contact.id)

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
