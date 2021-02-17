from django.shortcuts import render

# Create your views here.

def place_select(request):
    return render(request, 'place/place_select.html')
