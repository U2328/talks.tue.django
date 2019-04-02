from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericInlineModelAdmin

from .models import User, Subscription
from .forms import UserCreationForm, UserChangeForm



@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'collection',)
    list_filter = ('collection__is_meta', 'remind_me')
    fieldsets = (
        ('General', {'fields': ('user', 'collection')}),
        ('Config', {'classes': ('collapse',), 'fields': (('remind_me',),)}),
    )
    search_fields = ('user__username', 'collection__title')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'is_superuser', 'is_staff', 'is_verified')
    list_filter = ('is_superuser', 'is_staff', 'is_verified')
    fieldsets = (
        (None, {'fields': (('username', 'email', 'is_verified'),)}),
        ('User Role & Account Management', {'classes': ('collapse',), 'fields': (('is_superuser', 'is_staff',),)}),
        ('Important dates', {'classes': ('collapse',), 'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': (
            ('username', 'email', 'is_verified'),
            ('password1', 'password2')
        )}),
        ('User Role & Account Management', {'classes': ('collapse',), 'fields': (('is_superuser', 'is_staff',),)}),
    )
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    readonly_fields = ('last_login', 'date_joined')


admin.site.unregister(Group)