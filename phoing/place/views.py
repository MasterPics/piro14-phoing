from django.shortcuts import render
from .forms import PlaceForm

# Create your views here.


def place_select(request):

    form = PlaceForm()

    ctx = {
        'form': form,
    }
    return render(request, 'place/place_select.html', context=ctx)
