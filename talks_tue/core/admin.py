from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Talk, Collection, Tag, UserProfile, Subscription


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


class TalkAdmin(MarkdownModelAdmin, SimpleHistoryAdmin):
    ...


admin.site.register(Talk, TalkAdmin)


class CollectionAdmin(MarkdownModelAdmin, SimpleHistoryAdmin):
    ...


admin.site.register(Collection, CollectionAdmin)
admin.site.register(Tag)
admin.site.register(UserProfile)
admin.site.register(Subscription)
