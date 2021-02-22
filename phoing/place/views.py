from django.shortcuts import render, redirect, get_object_or_404
from .forms import LocationForm, PlaceForm
from django.contrib.auth.decorators import login_required
from myApp.models import Place, Tag
from django.contrib import messages
import json

# category filtering
from django.db.models import Count, Q

# infinite loading
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def place_create(request):

    if request.method == 'POST':
        place_form = PlaceForm(request.POST, request.FILES)
        location_form = LocationForm(request.POST)

        if place_form.is_valid() and location_form.is_valid():
            place = place_form.save(commit=False)
            location = location_form.save(commit=False)
            location.save()
            place.user = request.user
            place.location = location
            place.save()

            tags = Tag.add_tags(place.tag_str)
            for tag in tags:
                place.tags.add(tag)

            place.image = request.FILES.get('image')
            return redirect('place:place_detail', place.pk)

    else:
        place_form = PlaceForm()
        location_form = LocationForm()

    
    ctx = {
        'location_form': location_form,
        'place_form': place_form, 
    }

    return render(request, 'place/place_create.html', context=ctx)


def place_detail(request, pk):

    place = get_object_or_404(Place, pk=pk)
    request_user = request.user
    ctx = {
        'place' : place,
    }

    return render(request, 'place/place_detail.html', context=ctx)

@login_required
def place_update(request, pk):

    place = get_object_or_404(Place, pk=pk)
    
    if request.method == 'POST':
        place_form = PlaceForm(request.POST, request.FILES, instance=place)
        location_form = LocationForm(request.POST, instance=place.location)
        if place_form.is_valid() and location_form.is_valid():
            place = place_form.save(commit=False)
            location = location_form.save(commit=False)
            location.save()
            place.location = location
            place.image = request.FILES.get('image')

            place.tags.clear()
            tags = Tag.add_tags(place.tag_str)
            for tag in tags:
                place.tags.add(tag)

            place.save()
            return redirect('place:place_detail', place.pk)

    else:
        place_form = PlaceForm(instance=place)
        location_form = LocationForm(instance=place.location)

        ctx = {
        'place_form' : place_form,
        'location_form' : location_form,
        }
        
        return render(request, 'place/place_update.html', context=ctx)
            

    
def place_list(request):

    places = Place.objects.all()

    sort = request.GET.get('sort', 'recent')
    search = request.GET.get('search', '')

    # SORT
    if sort == 'pay':
        places = places.order_by('-pay', '-created_at')
    elif sort == 'recent':
        places = places.order_by('-created_at')

    if search:
        places = places.filter(
            Q(title__icontains=search) |  # 제목검색
            Q(desc__icontains=search) |  # 내용검색
            Q(user__username__icontains=search)  # 질문 글쓴이검색
        ).distinct()


    # infinite scroll
    places_per_page = 3
    page = request.GET.get('page', 1)
    paginator = Paginator(places, places_per_page)
    try:
        places = paginator.page(page)
    except PageNotAnInteger:
        places = paginator.page(1)
    except EmptyPage:
        places = paginator.page(paginator.num_pages)

    ctx = {
        'places': places,
        'sort': sort,
        'search': search,
    }

    return render(request, 'place/place_list.html', context=ctx)


@login_required
def place_delete(request, pk):

    place = get_object_or_404(Place, pk=pk)

    if request.method == 'POST':
        place.location.delete()
        place.delete()
        messages.success(request, '삭제되었습니다.')
        return redirect('place:place_list')
    
    else:
        ctx = {'place': place}
        return render(request, 'place/place_delete.html', context=ctx)



def place_map(request):

    places = Place.objects.all()

    ctx = {
        'places_json' : json.dumps([places.to_json() for place in places])
    }

    return render(request, 'place/place_map.html', context=ctx)



def place_select(request):

    form = LocationForm()

    ctx = {
        'form': form,
    }
    return render(request, 'place/place_select.html', context=ctx)

















