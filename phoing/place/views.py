from django.shortcuts import render
from .forms import LocationForm

# Create your views here.


def place_select(request):

    form = LocationForm()

    ctx = {
        'form': form,
    }
    return render(request, 'place/place_select.html', context=ctx)


def place_create(request):
    
    ctx = {

    }

    return render(request, 'place/place_create.html', context=ctx)


def place_list(request):
    
    ctx = {

    }

    return render(request, 'place/place_list.html', context=ctx)