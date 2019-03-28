from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from sequences import get_next_value
from markdownx.models import MarkdownxField
from simple_history.models import HistoricalRecords


__all__ = ("Talk", "MetaCollection", "Collection", "Tag", "Subscription")


class Talk(models.Model):
    class Meta:
        verbose_name = _("talk")
        verbose_name_plural = _("talks")

    title = models.CharField(verbose_name=_("Talk title"), max_length=128)
    description = MarkdownxField(verbose_name=_("Talk description"), max_length=512)
    timestamp = models.DateTimeField(verbose_name=_("Talk date"), default=now)
    name = models.CharField(verbose_name=_("Speaker's name"), max_length=128)
    about_me = MarkdownxField(verbose_name=_("Speaker's about me"), max_length=512)
    tags = models.ManyToManyField("Tag", verbose_name=_("Tags"), related_name="talks", blank=True)
    collections = models.ManyToManyField("Collection", verbose_name=_("Collections"), related_name="talks", blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class BaseCollection(models.Model):
    class Meta:
        abstract = True
    
    collection_id = models.IntegerField(unique=True)
    title = models.CharField(verbose_name=_("Title"), max_length=32)
    description = MarkdownxField(verbose_name=_("Description"), max_length=512)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL, null=True, blank=True, verbose_name=_("Oragnizer"), related_name="orgnized_%(class)ss"
    )
    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_("Editors"), related_name="edited_%(class)ss", blank=True
    )
    is_meta = models.BooleanField(verbose_name=_("Is metacollection?"), default=False)
    meta_collections = models.ManyToManyField(
        "MetaCollection", verbose_name=_("Metacollections"), related_name="sub_%(class)ss", blank=True
    )
    history = HistoricalRecords(inherit=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collection_id = get_next_value('collection_ids')

    def __str__(self):
        return self.title



class MetaCollection(BaseCollection):
    class Meta:
        verbose_name = _("meta collection")
        verbose_name_plural = _("meta collections")

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.is_meta = True

class Collection(BaseCollection):
    class Meta:
        verbose_name = _("collection")
        verbose_name_plural = _("collections")

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.is_meta = False

    @property
    def tags(self):
        return list(set(tag for talk in self.talks.all() for tag in talk.tags.all()))


class Tag(models.Model):
    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    name = models.CharField(verbose_name=_("Name"), max_length=32)

    def __str__(self):
        return self.name
