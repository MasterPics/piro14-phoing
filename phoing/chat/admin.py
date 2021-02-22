from django.contrib import admin

# Register your models here.
from .models import *



@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'contact', 'host']
    list_display_links = ['contact', 'host']
    



