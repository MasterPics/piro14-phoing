from django.urls import path
from . import views

app_name = 'place'

urlpatterns = [
    #####################profile#######################
    path('select/', view=views.place_select, name='place_select'),  # TODO : 나중에 삭제할 것


]
