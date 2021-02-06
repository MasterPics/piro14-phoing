from django.urls import path
from . import views

app_name = 'myApp'

urlpatterns = [
     path('', view=views.main_list, name='main_list'),
     path('profile/<int:pk>/', view=views.profile_detail, name='profile_detail'),
     path('profile/<int:pk>/delete',
         view=views.profile_delete, name='profile_delete'),
     path('profile/<int:pk>/portfolio',
         view=views.profile_portfolio, name='profile_portfolio'),
     path('profile/<int:pk>/update/',
         view=views.profile_update, name='profile_update'),
     path('profile/create/', view=views.profile_create, name='profile_create'),

     #####################contact#######################
     path('contact/', view=views.contact_list, name='contact_list'),
     path('contact/<int:pk>/', view=views.contact_detail, name='contact_detail'),
     path('contact/<int:pk>/delete',
         view=views.contact_delete, name='contact_delete'),
     path('contact/<int:pk>/update/',
         view=views.contact_update, name='contact_update'),
     path('contact/create/', view=views.contact_create, name='contact_create'),
     path('contact/save/', views.ContactSave.as_view(), name='contact_save'),

]
