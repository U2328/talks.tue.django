from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from sequences import get_next_value
from markdownx.models import MarkdownxField

from talks_tue.revisions.utils import HasRevision


__all__ = (
    "BaseTalk", "Talk",
    "BaseCollection", "MetaCollection", "Collection",
    "Tag"
)

# ========================
# Talks
# ========================

class BaseTalk(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(verbose_name=_("Talk title"), max_length=128)
    description = MarkdownxField(verbose_name=_("Talk description"), max_length=512)
    timestamp = models.DateTimeField(verbose_name=_("Talk date"), default=now)
    name = models.CharField(verbose_name=_("Speaker's name"), max_length=128)
    about_me = MarkdownxField(verbose_name=_("Speaker's about me"), max_length=512)
    tags = models.ManyToManyField("core.Tag", verbose_name=_("Tags"), related_name="tagged_%(class)s", blank=True)
    collections = models.ManyToManyField("core.Collection", verbose_name=_("Collections"), related_name="%(class)ss", blank=True)

    def __str__(self):
        return self.title


class Talk(HasRevision, BaseTalk):
    class Meta:
        ordering = ["timestamp"]
        verbose_name = _("talk")
        verbose_name_plural = _("talks")


# ========================
# Collections
# ========================

def _get_next_collection_id():
    return get_next_value('collection_ids')


class BaseCollection(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(verbose_name=_("Title"), max_length=32)
    description = MarkdownxField(verbose_name=_("Description"), max_length=512)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL, null=True, blank=True, verbose_name=_("Oragnizer"), related_name="organized_%(class)ss"
    )
    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_("Editors"), related_name="edited_%(class)ss", blank=True
    )
    is_meta = models.BooleanField(verbose_name=_("Is metacollection?"), default=False)
    meta_collections = models.ManyToManyField(
        "core.MetaCollection", verbose_name=_("Metacollections"), related_name="sub_%(class)ss", blank=True
    )

    def __str__(self):
        return self.title

# META -- NODE
class MetaCollection(HasRevision, BaseCollection):
    class Meta:
        verbose_name = _("meta collection")
        verbose_name_plural = _("meta collections")

    collection_id = models.IntegerField(default=_get_next_collection_id, primary_key=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_meta = True

    def save(self, *args, **kwargs):
        self.is_meta = True
        super().save(*args, **kwargs)


# NORMAL -- LEAF
class Collection(HasRevision, BaseCollection):
    class Meta:
        verbose_name = _("collection")
        verbose_name_plural = _("collections")

    collection_id = models.IntegerField(default=_get_next_collection_id, primary_key=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_meta = False

    @property
    def tags(self):
        return list(set(tag for talk in self.talks.all() for tag in talk.tags.all()))

    def save(self, *args, **kwargs):
        self.is_meta = False
        super().save(*args, **kwargs)

# ========================
# Misc
# ========================

class Tag(models.Model):
    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    name = models.CharField(verbose_name=_("Name"), max_length=32)

    def __str__(self):
        return self.name
