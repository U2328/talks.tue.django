from django.contrib import admin

from .utils import REVISION_MODEL_MAP


@admin.register(*REVISION_MODEL_MAP.values())
class RevisionAdmin(admin.ModelAdmin):
    list_display = (
        'original',
        'action',
        'user',
        'date_created',
    )
    list_filter = ('user', 'action')
    readonly_fields = ('action',)

