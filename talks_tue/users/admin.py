from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserCreationForm, UserChangeForm


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


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)