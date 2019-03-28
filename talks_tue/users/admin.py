from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericInlineModelAdmin

from .models import User, Subscription
from .forms import UserCreationForm, UserChangeForm



@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'collection',
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'is_admin',)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        ('User Role & Account Management', {'fields': ('is_admin',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'is_admin', 'password1', 'password2')}
         ),
    )
    search_fields = ('username',)
    ordering = ('-id',)
    filter_horizontal = ()
    readonly_fields = ('last_login', 'date_joined',)


admin.site.unregister(Group)