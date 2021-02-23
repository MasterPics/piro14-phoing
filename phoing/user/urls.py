from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'login'

urlpatterns = [
    path('login/', views.login_main, name='login_main'),
    path('signup/',views.login_main, name='signup_main'),
    path('login/form/', views.login_form, name='login_form'),
    path('signup/form/', views.signup_form, name='signup_form'),
    path('signup/form/social/', views.signup_form_social,name='signup_form_social'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('password/update/', views.password_update, name='password_upate'),



]


