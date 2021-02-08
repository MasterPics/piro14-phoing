from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import *

# User, Post, Contact, Portfolio, Comment, Tag, Image
# Register your models here.

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     pass


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('id',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title']
    list_display_links = ['title']
    search_fields = ['title']


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


'''
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first name', 'last_name', 'phone', 'email', 'password', 'category']
    list_display_links = ['username']
    search_fields = ['username']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title']
    list_display_links = ['title']
    search_fields = ['title']


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = PortfolioAdmin._meta.get_all_field_names()
    list_display_links = ['title']
    search_fields = ['title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = CommentAdmin._meta.get_all_field_names()
    list_display_links = ['post']
    search_fields = ['post']

    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = TagAdmin._meta.get_all_field_names()
    list_display_links = ['post']
    search_fields = ['post']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ImageAdmin._meta.get_all_field_names()
    list_display_links = ['post']
    search_fields = ['post']
    '''
