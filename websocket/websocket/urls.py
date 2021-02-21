from django.contrib import admin
from django.urls import path
from alarms import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('ShareMe', views.ShareMe.as_view()),
    path('Alarm', views.Alarm.as_view()),
]