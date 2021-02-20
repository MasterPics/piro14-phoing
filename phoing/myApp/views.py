from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import HttpResponse
from .forms import *
from user.models import *
from .models import *
import random
from django.http import JsonResponse

# for SAVE, LIKE
import json
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import login as auth_login
from place.forms import LocationForm


# category filtering
from django.db.models import Count, Q

# infinite loading
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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


def portfolio_list(request):
    portfolios = Portfolio.objects.all().order_by("?")
    request_user = request.user

    # category 분류 # order_by("?"): random 으로 선택
    category = request.GET.get('category', 'all')

    if category != 'all':
        if category == User.CATEGORY_PHOTOGRAPHER:
            portfolios = portfolios.filter(Q(user__category=User.CATEGORY_PHOTOGRAPHER)
                                           ).distinct().order_by("?")
        elif category == User.CATEGORY_MODEL:
            portfolios = portfolios.filter(Q(user__category=User.CATEGORY_MODEL)
                                           ).distinct().order_by("?")
        elif category == User.CATEGORY_HM:
            portfolios = portfolios.filter(Q(user__category=User.CATEGORY_HM)
                                           ).distinct().order_by("?")
        elif category == User.CATEGORY_STYLIST:
            portfolios = portfolios.filter(Q(user__category=User.CATEGORY_STYLIST)
                                           ).distinct().order_by("?")
        elif category == User.CATEGORY_OTHERS:
            portfolios = portfolios.filter(Q(user__category=User.CATEGORY_OTHERS)
                                           ).distinct().order_by("?")

    # SORT 최신순, 조회순, 좋아요순, 저장순
    sort = request.GET.get('sort', 'recent')

    if sort == 'recent':
        portfolios = portfolios.order_by('-updated_at')
    elif sort == 'view':
        portfolios = portfolios.annotate(num_save=Count(
            'view_count')).order_by('-num_save', '-updated_at')
    elif sort == 'like':
        portfolios = portfolios.annotate(num_save=Count(
            'like_users')).order_by('-num_save', '-updated_at')
    elif sort == 'save':
        portfolios = portfolios.annotate(num_save=Count(
            'save_users')).order_by('-num_save', '-updated_at')

    # infinite scroll
    portfolios_per_page = 3
    page = request.GET.get('page', 1)
    paginator = Paginator(portfolios, portfolios_per_page)
    try:
        portfolios = paginator.page(page)
    except PageNotAnInteger:
        portfolios = paginator.page(1)
    except EmptyPage:
        portfolios = paginator.page(paginator.num_pages)

    context = {'portfolios': portfolios, 'request_user': request_user, 'sort': sort,
               'category': category, }
    return render(request, 'myApp/portfolio/portfolio_list.html', context=context)


def portfolio_detail(request, pk):
    portfolio = Portfolio.objects.get(pk=pk)
    # tags=portfolio.tags.all()
    # TODO 태그, 추가 이미지 보이도록 tags = port.tags/images = port.images
    owner = portfolio.user
    owner_portfolios = Portfolio.objects.filter(user=owner)
    request_user = request.user
    ctx = {'portfolio': portfolio,
           'owner': owner,
           'tags': portfolio.tags.all(),
           'owner_portfolios': owner_portfolios,
           'request_user': request_user, }
    return render(request, 'myApp/portfolio/portfolio_detail.html', context=ctx)


@login_required
def portfolio_delete(request, pk):
    portfolio = Portfolio.objects.get(pk=pk)
    owner = portfolio.user
    if request.method == 'POST':
        portfolio.delete()
        messages.success(request, "삭제되었습니다.")
        return redirect('myApp:profile_portfolio', owner.id)
    else:
        ctx = {'portfolio': portfolio}
        return render(request, 'myApp/portfolio/portfolio_delete.html', context=ctx)


@login_required
def portfolio_update(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save()
            portfolio.image = request.FILES.get('image')
            portfolio.user = request.user
            portfolio.save()

            # save tag
            tags = Tag.add_tags(portfolio.tag_str)
            for tag in tags:
                portfolio.tags.add(tag)

            return redirect('myApp:portfolio_detail', portfolio.id)
    else:
        form = PortfolioForm()
        ctx = {'form': form}
        return render(request, 'myApp/portfolio/portfolio_update.html', ctx)


@login_required
def portfolio_create(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES,)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user

            portfolio.save()
            # portfolio.user.save()
            portfolio.image = request.FILES.get('image')

            # save tag
            tags = Tag.add_tags(portfolio.tag_str)
            for tag in tags:
                portfolio.tags.add(tag)

            return redirect('myApp:portfolio_detail', portfolio.pk)

    else:
        form = PortfolioForm()
        ctx = {'form': form}

    return render(request, 'myApp/portfolio/portfolio_create.html', ctx)

    portfolio.save_users = not portfolio.save_users
    portfolio.save()

    return JsonResponse({'id': portfolio_id, 'save_users': portfolio.save_users})


@csrf_exempt
def portfolio_save(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        portfolio_id = data["portfolio_id"]
        portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
        request_user = request.user
        is_saved = request_user in portfolio.save_users.all()
        if is_saved:
            portfolio.save_users.remove(
                get_object_or_404(User, pk=request_user.pk))
        else:
            portfolio.save_users.add(
                get_object_or_404(User, pk=request_user.pk))
        is_saved = not is_saved
        portfolio.save()
        return JsonResponse({'portfolio_id': portfolio_id, 'is_saved': is_saved})


@csrf_exempt
def portfolio_like(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        portfolio_id = data["portfolio_id"]
        portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
        request_user = request.user
        is_liked = request_user in portfolio.like_users.all()
        if is_liked:
            portfolio.like_users.remove(
                get_object_or_404(User, pk=request_user.pk))
        else:
            portfolio.like_users.add(
                get_object_or_404(User, pk=request_user.pk))
        is_liked = not is_liked
        portfolio.save()
        return JsonResponse({'portfolio_id': portfolio_id, 'is_liked': is_liked})


# TODO view_count 수정
@csrf_exempt
def portfolio_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        portfolio_id = data["portfolio_id"]
        portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
        request_user = request.user
        is_viewed = request_user in portfolio.view_count.all()
        portfolio.save_users.add(get_object_or_404(User, pk=request_user.pk))
        is_saved = not is_saved
        portfolio.save()
        return JsonResponse({'portfolio_id': portfolio_id, 'is_saved': is_saved})


###################### contact section ######################
@csrf_exempt
def contact_comment_create(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        contact_id = data["id"]
        comment_value = data["value"]
        contact = Contact.objects.get(id=contact_id)
        comment = Comment.objects.create(
            content=comment_value, contact=contact)
        return JsonResponse({'contact_id': contact_id, 'comment_id': comment.id, 'value': comment_value})


@csrf_exempt
def contact_comment_delete(request, pk):
    if request.method == 'POST':
        print('data is delivered')
        data = json.loads(request.body)
        comment_id = data["comment_id"]

        comment = Comment.objects.get(id=comment_id)
        comment.delete()

        return JsonResponse({'comment_id': comment_id})


@csrf_exempt
def contact_save(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        contact_id = data["contact_id"]
        contact = get_object_or_404(Contact, pk=contact_id)
        request_user = request.user
        is_saved = request_user in contact.save_users.all()
        if(is_saved):
            contact.save_users.remove(
                get_object_or_404(User, pk=request_user.pk))
        else:
            contact.save_users.add(get_object_or_404(User, pk=request_user.pk))
        is_saved = not is_saved
        contact.save()
        return JsonResponse({'contact_id': contact_id, 'is_saved': is_saved})


def contact_list(request):
    request_user = request.user
    contacts = Contact.objects.all()

    category = request.GET.get('category', 'all')  # CATEGORY
    sort = request.GET.get('sort', 'recent')  # SORT
    search = request.GET.get('search', '')  # SEARCH

    # CATEGORY
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
        elif category == User.CATEGORY_OTHERS:
            contacts = contacts.filter(Q(user__category=User.CATEGORY_OTHERS)
                                       ).distinct().order_by("?")

    # 카테고리가 없는 유저들이 other use는 아님. 따로 있다!
    # SORT
    if sort == 'save':
        contacts = contacts.annotate(num_save=Count(
            'save_users')).order_by('-num_save', '-created_at')
    elif sort == 'pay':
        contacts = contacts.order_by('-pay', '-created_at')
    elif sort == 'recent':
        contacts = contacts.order_by('-created_at')

    # SEARCH
    if search:
        contacts = contacts.filter(
            Q(title__icontains=search) |  # 제목검색
            Q(desc__icontains=search) |  # 내용검색
            Q(user__username__icontains=search)  # 질문 글쓴이검색
        ).distinct()

    # infinite scroll
    contacts_per_page = 3
    page = request.GET.get('page', 1)
    paginator = Paginator(contacts, contacts_per_page)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    context = {
        'contacts': contacts,
        'sort': sort,
        'category': category,
        'search': search,
        'request_user': request_user,
    }
    return render(request, 'myApp/contact/contact_list.html', context=context)


def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    request_user = request.user
    ctx = {
        'contact': contact,
        'request_user': request_user,
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
            return redirect('myApp:contact_detail', contact.pk)
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
        location_form = LocationForm(request.POST)

        if contact_form.is_valid() and location_form.is_valid():
            print('here')
            contact = contact_form.save(commit=False)
            location = location_form.save(commit=False)
            location.save()
            contact.user = request.user
            contact.is_closed = False
            contact.location = location
            contact.save()
            contact.image = request.FILES.get('image')
            return redirect('myApp:contact_detail', contact.pk)

    else:
        contact_form = ContactForm()
        location_form = LocationForm()

    return render(request, 'myApp/contact/contact_create.html', {'contact_form': contact_form, 'location_form': location_form})


# # @login_required
# class ContactSave(View):
#     template_name = 'contact/contact_list.html'

#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super(ContactSave, self).dispatch(request, *args, **kwargs)

#     def get(self, request):
#         contacts = Contact.objects.all()
#         ctx = {"contacts": contacts}
#         return render(request, self.template_name, ctx)

#     def post(self, request):
#         data = json.loads(request.body)
#         contact_id = data["id"]
#         contact = Contact.objects.get(id=contact_id)
#         save_users = contact.save_users.all()
#         if user.is_authenticated():
#             if request.user in save_user:
#                 contact.save()

#         return JsonResponse({'id': contact_id, 'save_users': contact.save_users})


def contact_map(request):

    contacts = Contact.objects.filter(is_closed=False)

    ctx = {
        'contacts_json': json.dumps([contact.to_json() for contact in contacts])
    }

    return render(request, 'myApp/contact/contact_map.html', context=ctx)
