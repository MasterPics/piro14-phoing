from django.urls import path, include
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm
from django.views.generic import TemplateView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=UserLoginForm),
        name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
