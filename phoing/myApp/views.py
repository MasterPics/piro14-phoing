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
from .utils import *
from place.forms import LocationForm

# category filtering
from django.db.models import Count, Q

# infinite loading
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# for multiple images
from django.forms import modelformset_factory


def main_list(request):
    ctx = {}
    return render(request, 'myApp/main/main_list.html', context=ctx)

###################### profile section ######################


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
def profile_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    ctx = {'user': user, }
    return render(request, 'myApp/profile/profile_detail.html', context=ctx)


@login_required
def profile_detail_posts(request, pk):
    user = get_object_or_404(User, pk=pk)

    category = request.GET.get('category', 'contact')  # CATEGORY
    # sort = request.GET.get('sort', 'recent')  # SORT
    search = request.GET.get('search', '')  # SEARCH

    # CATEGORY
    if category == 'contact':
        posts = user.contacts.all().order_by("?")
    elif category == 'portfolio':
        posts = user.portfolios.all().order_by("?")

    # SORT

    # SEARCH

    # infinite scroll

    ctx = {
        'user': user,
        'posts': posts,
        'category': category,
    }
    return render(request, 'myApp/profile/profile_detail_posts.html', context=ctx)


def profile_detail_other(request, pk):
    user = User.objects.get(pk=pk)
    portfolios = user.portfolios.all()
    # portfolios = Portfolio.objects.filter(user=user)
    ctx = {'user': user, 'portfolios': portfolios}
    return render(request, 'myApp/profile/profile_detail_other.html', context=ctx)


@login_required
def post_create(request):
    if request.method == 'POST':
        messages.success(request, "create your post!")
    else:
        ctx = {}
        return render(request, 'myApp/profile/post_create.html', context=ctx)

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

    context = {'portfolios': portfolios, 'request_user': request.user, 'sort': sort,
               'category': category, }
    return render(request, 'myApp/portfolio/portfolio_list.html', context=context)


def portfolio_detail(request, pk):
    portfolio = Portfolio.objects.get(pk=pk)
    images = portfolio.portfolio_images.all()
    num_of_imgs = images.count

    tags = portfolio.tags.all()

    portfolio_owner = portfolio.user  # 게시글 작성자
    request_user = request.user  # 로그인한 유저
    ctx = {'portfolio': portfolio,
           'images': images,
           'tags': tags,
           'portfolio_owner': portfolio_owner,
           'request_user': request_user,
           'num_of_imgs': num_of_imgs, }
    return render(request, 'myApp/portfolio/portfolio_detail.html', context=ctx)


@login_required
def portfolio_delete(request, pk):
    portfolio = Portfolio.objects.get(pk=pk)
    owner = portfolio.user
    if request.method == 'POST':
        portfolio.delete()
        messages.success(request, "삭제되었습니다.")
        return redirect('myApp:profile_detail_posts', owner.id)
    else:
        ctx = {'portfolio': portfolio}
        return render(request, 'myApp/portfolio/portfolio_delete.html', context=ctx)


@login_required
def portfolio_update(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=10)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())
        if form.is_valid() and formset.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
            portfolio.image = request.FILES.get('image')
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = Images(portfolio=portfolio, image=image)
                    photo.save()
            messages.success(request, "posted!")

            # save tag
            tags = Tag.add_tags(portfolio.tag_str)
            for tag in tags:
                portfolio.tags.add(tag)

            return redirect('myApp:portfolio_detail', portfolio.id)
    else:
        form = PortfolioForm(instance=portfolio)
        formset = ImageFormSet(
            queryset=Images.objects.none())
        ctx = {'form': form, 'formset': formset}
        return render(request, 'myApp/portfolio/portfolio_update.html', ctx)


@login_required
def portfolio_create(request):
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=10)
    # 'extra' : number of photos
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES,)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())

        if form.is_valid() and formset.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
            portfolio.image = request.FILES.get('image')
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = Images(portfolio=portfolio, image=image)
                    photo.save()
            messages.success(request, "posted!")

            # save tag
            tags = Tag.add_tags(portfolio.tag_str)
            for tag in tags:
                portfolio.tags.add(tag)

            return redirect('myApp:portfolio_detail', portfolio.pk)
        else:
            print(form.errors, formset.errors)
    else:
        form = PortfolioForm()
        formset = ImageFormSet(queryset=Images.objects.none())
        ctx = {'form': form, 'formset': formset}

    return render(request, 'myApp/portfolio/portfolio_create.html', ctx)


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
        is_saved = request.user in contact.save_users.all()
        if(is_saved):
            contact.save_users.remove(
                get_object_or_404(User, pk=request.user.pk))
        else:
            contact.save_users.add(get_object_or_404(User, pk=request.user.pk))
        is_saved = not is_saved
        contact.save()
        return JsonResponse({'contact_id': contact_id, 'is_saved': is_saved})


def contact_list(request):
    contacts = Contact.objects.all()

    category = request.GET.get('category', 'all')  # CATEGORY
    sort = request.GET.get('sort', 'recent')  # SORT
    search = request.GET.get('search', '')  # SEARCH
    no_pay = request.GET.get('no_pay', False)
    if no_pay == 'true':
        contacts = Contact.objects.all().filter(pay=0).distinct()
    else:
        contacts = Contact.objects.all()

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
    contacts_per_page = 1
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
        'request_user': request.user,
    }
    return render(request, 'myApp/contact/contact_list.html', context=context)


def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    # contact_owner = contact.user  # contact 게시글 작성자

    tags = contact.tags.all()

    ctx = {
        'contact': contact,
        # 'contact_owner': contact_owner,
        'request_user': request.user,
        'tags': tags,
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
            contact.image = request.FILES.get('image')
            contact = form.save()

            # save tag
            tags = Tag.add_tags(contact.tag_str)
            for tag in tags:
                contact.tags.add(tag)

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

            # save tag
            tags = Tag.add_tags(contact.tag_str)
            for tag in tags:
                contact.tags.add(tag)

            return redirect('myApp:contact_detail', contact.pk)

    else:
        contact_form = ContactForm()
        location_form = LocationForm()

    return render(request, 'myApp/contact/contact_create.html', {'contact_form': contact_form, 'location_form': location_form})


def contact_map(request):

    contacts = Contact.objects.filter(is_closed=False)

    ctx = {
        'contacts_json': json.dumps([contact.to_json() for contact in contacts])
    }

    return render(request, 'myApp/contact/contact_map.html', context=ctx)


###################### reference section ######################
def reference_list(request):
    references = Reference.objects.all()

    context = {
        'references': references,
        'request_user': request.user,
    }
    return render(request, 'myApp/reference/reference_list.html', context=context)


def reference_detail(request, pk):
    reference = get_object_or_404(Reference, pk=pk)
    reference_image_urls = reference.image_url

    # infinite scroll
    reference_image_per_page = 20
    page = request.GET.get('page', 1)
    paginator = Paginator(reference_image_urls, reference_image_per_page)
    try:
        reference_image_urls = paginator.page(page)
    except PageNotAnInteger:
        reference_image_urls = paginator.page(1)
    except EmptyPage:
        reference_image_urls = paginator.page(paginator.num_pages)

    ctx = {
        'reference': reference,
        'reference_image_urls': reference_image_urls,
        'idx': range(20),
    }
    return render(request, 'myApp/reference/reference_detail.html', context=ctx)

    ###################### collabration section ######################
    ###################### 1. with brand        ######################
    ###################### with_brand section   ######################


@csrf_exempt
def with_brand_comment_create(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        with_brand_id = data["id"]
        comment_value = data["value"]
        with_brand = CollaborationWithBrand.objects.get(id=with_brand_id)
        comment = Comment.objects.create(
            content=comment_value, with_brand=with_brand)
        return JsonResponse({'with_brand_id': with_brand_id, 'comment_id': comment.id, 'value': comment_value})


@csrf_exempt
def with_brand_comment_delete(request, pk):
    if request.method == 'POST':
        print('data is delivered')
        data = json.loads(request.body)
        comment_id = data["comment_id"]

        comment = Comment.objects.get(id=comment_id)
        comment.delete()

        return JsonResponse({'comment_id': comment_id})


@csrf_exempt
def with_brand_save(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        with_brand_id = data["with_brand_id"]
        with_brand = get_object_or_404(
            CollaborationWithBrand, pk=with_brand_id)
        is_saved = request.user in with_brand.save_users.all()
        if(is_saved):
            with_brand.save_users.remove(
                get_object_or_404(User, pk=request.user.pk))
        else:
            with_brand.save_users.add(
                get_object_or_404(User, pk=request.user.pk))
        is_saved = not is_saved
        with_brand.save()
        return JsonResponse({'with_brand_id': with_brand_id, 'is_saved': is_saved})


def with_brand_list(request):
    with_brands = CollaborationWithBrand.objects.all()

    category = request.GET.get('category', 'all')  # CATEGORY
    sort = request.GET.get('sort', 'recent')  # SORT
    search = request.GET.get('search', '')  # SEARCH
    no_pay = request.GET.get('no_pay', False)
    print(type(no_pay), no_pay)
    if no_pay == 'true':
        with_brands = CollaborationWithBrand.objects.all().filter(pay=0).distinct()
    else:
        with_brands = CollaborationWithBrand.objects.all()

    # CATEGORY
    if category != 'all':
        if category == User.CATEGORY_PHOTOGRAPHER:
            with_brands = with_brands.filter(Q(user__category=User.CATEGORY_PHOTOGRAPHER)
                                             ).distinct().order_by("?")
        elif category == User.CATEGORY_MODEL:
            with_brands = with_brands.filter(Q(user__category=User.CATEGORY_MODEL)
                                             ).distinct().order_by("?")
        elif category == User.CATEGORY_HM:
            with_brands = with_brands.filter(Q(user__category=User.CATEGORY_HM)
                                             ).distinct().order_by("?")
        elif category == User.CATEGORY_STYLIST:
            with_brands = with_brands.filter(Q(user__category=User.CATEGORY_STYLIST)
                                             ).distinct().order_by("?")
        elif category == User.CATEGORY_OTHERS:
            with_brands = with_brands.filter(Q(user__category=User.CATEGORY_OTHERS)
                                             ).distinct().order_by("?")

    # 카테고리가 없는 유저들이 other use는 아님. 따로 있다!
    # SORT
    if sort == 'save':
        with_brands = with_brands.annotate(num_save=Count(
            'save_users')).order_by('-num_save', '-created_at')
    elif sort == 'pay':
        with_brands = with_brands.order_by('-pay', '-created_at')
    elif sort == 'recent':
        with_brands = with_brands.order_by('-created_at')

    # SEARCH
    if search:
        with_brands = with_brands.filter(
            Q(title__icontains=search) |  # 제목검색
            Q(desc__icontains=search) |  # 내용검색
            Q(user__username__icontains=search)  # 질문 글쓴이검색
        ).distinct()

    # # infinite scroll
    # with_brands_per_page = 3
    # page = request.GET.get('page', 1)
    # paginator = Paginator(with_brands, with_brands_per_page)
    # try:
    #     with_brands = paginator.page(page)
    # except PageNotAnInteger:
    #     with_brands = paginator.page(1)
    # except EmptyPage:
    #     with_brands = paginator.page(paginator.num_pages)

    context = {
        'with_brands': with_brands,
        'sort': sort,
        'category': category,
        'search': search,
        'request_user': request.user,
    }
    return render(request, 'myApp/with_brand/with_brand_list.html', context=context)


def with_brand_detail(request, pk):
    with_brand = get_object_or_404(CollaborationWithBrand, pk=pk)
    ctx = {
        'with_brand': with_brand,
        'request_user': request.user,
    }
    return render(request, 'myApp/with_brand/with_brand_detail.html', context=ctx)


@login_required
def with_brand_delete(request, pk):
    with_brand = get_object_or_404(CollaborationWithBrand, pk=pk)
    if request.method == 'POST':
        with_brand.delete()
        messages.success(request, "탈퇴되었습니다.")
        return redirect('myApp:with_brand_list')
    else:
        ctx = {'with_brand': with_brand}
        return render(request, 'myApp/with_brand/with_brand_delete.html', context=ctx)


@login_required
def with_brand_update(request, pk):
    with_brand = get_object_or_404(CollaborationWithBrand, pk=pk)
    if request.method == 'POST':
        form = WithBrandForm(
            request.POST, request.FILES, instance=with_brand)
        if form.is_valid():
            with_brand.image = request.FILES.get('image')
            with_brand = form.save()
            # save tag
            tags = Tag.add_tags(with_brand.tag_str)
            for tag in tags:
                with_brand.tags.add(tag)

            return redirect('myApp:with_brand_detail', with_brand.pk)
    else:
        form = WithBrandForm(instance=with_brand)
        ctx = {'form': form}
        return render(request, 'myApp/with_brand/with_brand_update.html', ctx)


@login_required
def with_brand_create(request):
    # if request.user.is_authenticated:
    #     return redirect('myApp:profile_detail')

    if request.method == 'POST':
        with_brand_form = WithBrandForm(
            request.POST, request.FILES)
        location_form = LocationForm(request.POST)

        if with_brand_form.is_valid() and location_form.is_valid():
            print('here')
            with_brand = with_brand_form.save(commit=False)
            location = location_form.save(commit=False)
            location.save()
            with_brand.user = request.user
            with_brand.is_closed = False
            with_brand.location = location
            with_brand.save()
            with_brand.image = request.FILES.get('image')

            # save tag
            tags = Tag.add_tags(with_brand.tag_str)
            for tag in tags:
                with_brand.tags.add(tag)

            return redirect('myApp:with_brand_detail', with_brand.pk)

    else:
        with_brand_form = WithBrandForm()
        location_form = LocationForm()

    return render(request, 'myApp/with_brand/with_brand_create.html', {'with_brand_form': with_brand_form, 'location_form': location_form})


def with_brand_map(request):

    with_brands = CollaborationWithBrand.objects.filter(is_closed=False)

    ctx = {
        'with_brands_json': json.dumps([with_brand.to_json() for with_brand in with_brands])
    }

    return render(request, 'myApp/with_brand/with_brand_map.html', context=ctx)

    ###################### 2. with artist       ######################


@csrf_exempt
def with_artist_comment_create(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        with_artist_id = data["id"]
        comment_value = data["value"]
        with_artist = CollaborationWithArtist.objects.get(id=with_artist_id)
        comment = Comment.objects.create(
            content=comment_value, with_artist=with_artist)
        return JsonResponse({'with_artist_id': with_artist_id, 'comment_id': comment.id, 'value': comment_value})


@csrf_exempt
def with_artist_comment_delete(request, pk):
    if request.method == 'POST':
        print('data is delivered')
        data = json.loads(request.body)
        comment_id = data["comment_id"]

        comment = Comment.objects.get(id=comment_id)
        comment.delete()

        return JsonResponse({'comment_id': comment_id})


@csrf_exempt
def with_artist_save(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        with_artist_id = data["with_artist_id"]
        with_artist = get_object_or_404(
            CollaborationWithArtist, pk=with_artist_id)
        is_saved = request.user in with_artist.save_users.all()
        if(is_saved):
            with_artist.save_users.remove(
                get_object_or_404(User, pk=request.user.pk))
        else:
            with_artist.save_users.add(
                get_object_or_404(User, pk=request.user.pk))
        is_saved = not is_saved
        with_artist.save()
        return JsonResponse({'with_artist_id': with_artist_id, 'is_saved': is_saved})


def with_artist_list(request):
    with_artists = CollaborationWithArtist.objects.all()

    category = request.GET.get('category', 'all')  # CATEGORY
    sort = request.GET.get('sort', 'recent')  # SORT
    search = request.GET.get('search', '')  # SEARCH
    no_pay = request.GET.get('no_pay', False)
    print(type(no_pay), no_pay)
    if no_pay == 'true':
        with_artists = CollaborationWithArtist.objects.all().filter(pay=0).distinct()
    else:
        with_artists = CollaborationWithArtist.objects.all()

    # CATEGORY
    if category != 'all':
        if category == User.CATEGORY_PHOTOGRAPHER:
            with_artists = with_artists.filter(Q(user__category=User.CATEGORY_PHOTOGRAPHER)
                                               ).distinct().order_by("?")
        elif category == User.CATEGORY_MODEL:
            with_artists = with_artists.filter(Q(user__category=User.CATEGORY_MODEL)
                                               ).distinct().order_by("?")
        elif category == User.CATEGORY_HM:
            with_artists = with_artists.filter(Q(user__category=User.CATEGORY_HM)
                                               ).distinct().order_by("?")
        elif category == User.CATEGORY_STYLIST:
            with_artists = with_artists.filter(Q(user__category=User.CATEGORY_STYLIST)
                                               ).distinct().order_by("?")
        elif category == User.CATEGORY_OTHERS:
            with_artists = with_artists.filter(Q(user__category=User.CATEGORY_OTHERS)
                                               ).distinct().order_by("?")

    # 카테고리가 없는 유저들이 other use는 아님. 따로 있다!
    # SORT
    if sort == 'save':
        with_artists = with_artists.annotate(num_save=Count(
            'save_users')).order_by('-num_save', '-created_at')
    elif sort == 'pay':
        with_artists = with_artists.order_by('-pay', '-created_at')
    elif sort == 'recent':
        with_artists = with_artists.order_by('-created_at')

    # SEARCH
    if search:
        with_artists = with_artists.filter(
            Q(title__icontains=search) |  # 제목검색
            Q(desc__icontains=search) |  # 내용검색
            Q(user__username__icontains=search)  # 질문 글쓴이검색
        ).distinct()

    # # infinite scroll
    # with_artists_per_page = 3
    # page = request.GET.get('page', 1)
    # paginator = Paginator(with_artists, with_artists_per_page)
    # try:
    #     with_artists = paginator.page(page)
    # except PageNotAnInteger:
    #     with_artists = paginator.page(1)
    # except EmptyPage:
    #     with_artists = paginator.page(paginator.num_pages)

    context = {
        'with_artists': with_artists,
        'sort': sort,
        'category': category,
        'search': search,
        'request_user': request.user,
    }
    return render(request, 'myApp/with_artist/with_artist_list.html', context=context)


def with_artist_detail(request, pk):
    with_artist = get_object_or_404(CollaborationWithArtist, pk=pk)
    ctx = {
        'with_artist': with_artist,
        'request_user': request.user,
    }
    return render(request, 'myApp/with_artist/with_artist_detail.html', context=ctx)


@login_required
def with_artist_delete(request, pk):
    with_artist = get_object_or_404(CollaborationWithArtist, pk=pk)
    if request.method == 'POST':
        with_artist.delete()
        messages.success(request, "탈퇴되었습니다.")
        return redirect('myApp:with_artist_list')
    else:
        ctx = {'with_artist': with_artist}
        return render(request, 'myApp/with_artist/with_artist_delete.html', context=ctx)


@login_required
def with_artist_update(request, pk):
    with_artist = get_object_or_404(CollaborationWithArtist, pk=pk)
    if request.method == 'POST':
        form = WithArtistForm(
            request.POST, request.FILES, instance=with_artist)
        if form.is_valid():
            with_artist.image = request.FILES.get('image')
            with_artist = form.save()
            tags = Tag.add_tags(with_artist.tag_str)
            for tag in tags:
                with_artist.tags.add(tag)

            return redirect('myApp:with_artist_detail', with_artist.pk)
    else:
        form = WithArtistForm(instance=with_artist)
        ctx = {'form': form}
        return render(request, 'myApp/with_artist/with_artist_update.html', ctx)


@login_required
def with_artist_create(request):
    # if request.user.is_authenticated:
    #     return redirect('myApp:profile_detail')

    if request.method == 'POST':
        with_artist_form = WithArtistForm(
            request.POST, request.FILES)
        location_form = LocationForm(request.POST)

        if with_artist_form.is_valid() and location_form.is_valid():
            print('here')
            with_artist = with_artist_form.save(commit=False)
            location = location_form.save(commit=False)
            location.save()
            with_artist.user = request.user
            with_artist.is_closed = False
            with_artist.location = location
            with_artist.save()
            with_artist.image = request.FILES.get('image')
            # save tag
            tags = Tag.add_tags(with_artist.tag_str)
            for tag in tags:
                with_artist.tags.add(tag)

            return redirect('myApp:with_artist_detail', with_artist.pk)

    else:
        with_artist_form = WithArtistForm()
        location_form = LocationForm()

    return render(request, 'myApp/with_artist/with_artist_create.html', {'with_artist_form': with_artist_form, 'location_form': location_form})


def with_artist_map(request):

    with_artists = CollaborationWithArtist.objects.filter(is_closed=False)

    ctx = {
        'with_artists_json': json.dumps([with_artist.to_json() for with_artist in with_artists])
    }

    return render(request, 'myApp/with_artist/with_artist_map.html', context=ctx)
