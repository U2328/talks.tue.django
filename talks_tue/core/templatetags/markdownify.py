from functools import partial

from django.conf import settings
from django.utils.safestring import mark_safe

import markdown
import bleach

from . import register

@register.filter
def markdownify(text):
    """A simple filter to translate markdown into HTML.
    
    Taken and adapted from django-markdownify
    """
    # Markdown settings
    strip = getattr(settings, 'MARKDOWNIFY_STRIP', True)
    extensions = getattr(settings, 'MARKDOWNIFY_MARKDOWN_EXTENSIONS', [])
    extension_configs = getattr(settings, 'MARKDOWNIFY_MARKDOWN_EXTENSION_CONFIGS', [])

    # Convert markdown to html
    html = markdown.markdown(text, extensions=extensions, extension_configs=extension_configs)

    return mark_safe(html)