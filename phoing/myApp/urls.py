from django.urls import path
from . import views

app_name = 'myApp'

urlpatterns = [
    #####################profile#######################
    path('', view=views.main_list, name='main_list'),
    path('profile/<int:pk>/', view=views.profile_detail, name='profile_detail'),
    path('profile/<int:pk>/posts/',
         view=views.profile_detail_posts, name='profile_detail_posts'),
     path('profile/<int:pk>/saves/',
         view=views.profile_detail_saves, name='profile_detail_saves'),
    path('profile/<int:pk>/delete/',
         view=views.profile_delete, name='profile_delete'),
    path('profile/<int:pk>/update/',
         view=views.profile_update, name='profile_update'),
    path('profile/<int:pk>/profile_update_password/',
         view=views.profile_update_password, name='profile_update_password'),
    path('profile/create/', view=views.profile_create, name='profile_create'),
    path('profile/post/create/', view=views.post_create, name='post_create'),

    #####################contact#######################
    path('contact/', view=views.contact_list, name='contact_list'),
    #path('contact/<string:category>', view=views.contact_category, name='contact_category'),
    path('contact/map/', view=views.contact_map, name='contact_map'),
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

    #####################reference#######################
    #1. from phoging(local) #
    path('local/', view=views.local_list, name='local_list'),
    path('local/<slug:tag>/', view=views.local_detail, name='local_detail'),


    #2. from reference(pinterest) #
    path('reference/', view=views.reference_list, name='reference_list'),
    path('reference/detail/<int:pk>/',
         view=views.reference_detail, name='reference_detail'),

    #####################collaborations#######################

    #1. with brand #
    path('with_brand/', view=views.with_brand_list, name='with_brand_list'),
    #path('with_brand/<string:category>', view=views.with_brand_category, name='with_brand_category'),
    path('with_brand/map/', view=views.with_brand_map, name='with_brand_map'),
    path('with_brand/detail/<int:pk>/',
         view=views.with_brand_detail, name='with_brand_detail'),
    path('with_brand/<int:pk>/comment_create/',
         view=views.with_brand_comment_create, name='with_brand_comment_create'),
    path('with_brand/<int:pk>/comment_delete/',
         view=views.with_brand_comment_delete, name='with_brand_comment_delete'),
    path('with_brand/<int:pk>/delete/',
         view=views.with_brand_delete, name='with_brand_delete'),
    path('with_brand/<int:pk>/update/',
         view=views.with_brand_update, name='with_brand_update'),
    path('with_brand/create/', view=views.with_brand_create,
         name='with_brand_create'),
    path('with_brand/save/', view=views.with_brand_save, name='with_brand_save'),

    #2. with artist #
    path('with_artist/', view=views.with_artist_list, name='with_artist_list'),
    #path('with_artist/<str2aing:category>', view=views.with_artist_category, name='with_artist_category'),
    path('with_artist/map/', view=views.with_artist_map,
         name='with_artist_map'),
    path('with_artist/detail/<int:pk>/',
         view=views.with_artist_detail, name='with_artist_detail'),
    path('with_artist/<int:pk>/comment_create/',
         view=views.with_artist_comment_create, name='with_artist_comment_create'),
    path('with_artist/<int:pk>/comment_delete/',
         view=views.with_artist_comment_delete, name='with_artist_comment_delete'),
    path('with_artist/<int:pk>/delete/',
         view=views.with_artist_delete, name='with_artist_delete'),
    path('with_artist/<int:pk>/update/',
         view=views.with_artist_update, name='with_artist_update'),
    path('with_artist/create/', view=views.with_artist_create,
         name='with_artist_create'),
    path('with_artist/save/', view=views.with_artist_save,
         name='with_artist_save'),

]
