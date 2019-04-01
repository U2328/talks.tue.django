from django.contrib import admin

from .utils import REVISION_MODEL_MAP


@admin.register(*REVISION_MODEL_MAP.values())
class RevisionAdmin(admin.ModelAdmin):
    list_display = (
        'original',
        'create',
        'user',
    )
    fieldsets = tuple()
    list_filter = ('user',)

    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True
