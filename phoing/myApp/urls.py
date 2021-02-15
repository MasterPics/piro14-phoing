from django.urls import path
from . import views

app_name = 'myApp'

urlpatterns = [
    #####################profile#######################
    path('', view=views.main_list, name='main_list'),
    path('profile/<int:pk>/', view=views.profile_detail, name='profile_detail'),
    path('profile/<int:pk>/other', view=views.profile_detail_other,
         name='profile_detail_other'),
    path('profile/<int:pk>/delete/',
         view=views.profile_delete, name='profile_delete'),
    path('profile/<int:pk>/portfolio/',
         view=views.profile_portfolio, name='profile_portfolio'),
    path('profile/<int:pk>/update/',
         view=views.profile_update, name='profile_update'),
    path('profile/create/', view=views.profile_create, name='profile_create'),

    #####################contact#######################
    path('contact/', view=views.contact_list, name='contact_list'),
    #path('contact/<string:category>', view=views.contact_category, name='contact_category'),
    path('contact/detail/<int:pk>/',
         view=views.contact_detail, name='contact_detail'),
    path('contact/<int:pk>/comment_create/',
         view=views.contact_comment_create, name='contact_comment_create'),
    path('contact/<int:pk>/comment_delete/',
         view=views.contact_comment_delete, name='contact_comment_delete'),
    path('contact/<int:pk>/delete/',
         view=views.contact_delete, name='contact_delete'),
    path('contact/<int:pk>/update/',
         view=views.contact_update, name='contact_update'),
    path('contact/create/', view=views.contact_create, name='contact_create'),
    path('contact/save/', views.contact_save, name='contact_save'),

    #####################portfolio#######################
    path('portfolio/',
         view=views.portfolio_list, name='portfolio_list'),
    path('portfolio/<int:pk>/', view=views.portfolio_detail,
         name='portfolio_detail'),
    path('portfolio/<int:pk>/delete/',
         view=views.portfolio_delete, name='portfolio_delete'),
    path('portfolio/<int:pk>/update/',
         view=views.portfolio_update, name='portfolio_update'),
    path('portfolio/create/', view=views.portfolio_create, name='portfolio_create'),
    path('portfolio/like/', view=views.portfolio_like,
         name='portfolio_like'),
    path('portfolio/save/', view=views.portfolio_save,
         name='portfolio_save'),
]
