from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Talk, Collection, MetaCollection, Tag


class MarkdownModelAdmin(MarkdownxModelAdmin):
    class Media:
        js = (
            "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.9.0/katex.min.js",
            "/static/js/setup_katex.js",
        )
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.9.0/katex.min.css',
                '/static/css/pygments_default.css',
            )
        }


@admin.register(Talk)
class TalkAdmin(MarkdownModelAdmin):
    list_display = (
        'title',
        'name',
        'timestamp',
    )
    fieldsets = (
        ('Talk Info', {'fields': ('title', 'timestamp', 'description')}),
        ('Speaker Info', {'fields': ('name', 'about_me')}),
        ('Links', {'fields': ('collections', 'tags')}),
    )
    list_filter = tuple()
    raw_id_fields = tuple()

@admin.register(Collection, MetaCollection)
class CollectionAdmin(MarkdownModelAdmin):
    list_display = (
        'collection_id',
        'title',
        'description',
        'organizer',
    )
    fieldsets = (
        (None, {'fields': ('title', 'description')}),
        ('Related Users', {'fields': ('organizer', 'editors')}),
        ('Related Collections', {'fields': ('meta_collections',)}),
    )
    list_filter = ('organizer', 'is_meta')
    raw_id_fields = tuple()

admin.site.register(Tag)
