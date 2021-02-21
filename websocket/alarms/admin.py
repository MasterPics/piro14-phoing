from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import *

@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    pass