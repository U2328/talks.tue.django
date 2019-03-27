from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from simple_history.models import HistoricalRecords


__all__ = ("Talk", "Collection", "Tag", "Subscription")


class Talk(models.Model):
    class Meta:
        verbose_name = _("talk")
        verbose_name_plural = _("talks")

    title = models.CharField(verbose_name=_("Talk title"), max_length=128)
    description = MarkdownxField(verbose_name=_("Talk description"), max_length=512)
    timestamp = models.DateTimeField(verbose_name=_("Talk date"), default=now)
    name = models.CharField(verbose_name=_("Speaker's name"), max_length=128)
    about_me = MarkdownxField(verbose_name=_("Speaker's about me"), max_length=512)
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class Collection(models.Model):
    class Meta:
        verbose_name = _("collection")
        verbose_name_plural = _("collections")

    title = models.CharField(verbose_name=_("Title"), max_length=32)
    description = MarkdownxField(verbose_name=_("Description"), max_length=512)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL, null=True, blank=True, verbose_name=_("Oragnizer"), related_name="orgnized_collections"
    )
    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_("Editors"), related_name="edited_collections"
    )
    is_meta = models.BooleanField(verbose_name=_("Is metacollection?"), default=False)
    history = HistoricalRecords()

    talks = models.ManyToManyField(
        "Talk", null=True, blank=True, verbose_name=_("Talks"), related_name="collections"
    )
    sub_collections = models.ManyToManyField(
        "Collection", null=True, blank=True, verbose_name=_("Subcollections"), related_name="meta_collections"
    )

    def save(self, *args, **kwargs):
        if self.is_meta:
            self.talks.clear()
            self.sub_collections.remove(self)
        else:
            self.sub_collections.clear()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def tags(self):
        return list(set(tag for talk in self.talks.all() for tag in talk.tags.all()))


class Tag(models.Model):
    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    name = models.CharField(verbose_name=_("Name"), max_length=32)
    talks = models.ManyToManyField("Talk", verbose_name=_("Talks"), related_name="tags")

    def __str__(self):
        return self.name


class Subscription(models.Model):
    class Meta:
        verbose_name = _("subscription")
        verbose_name_plural = _("subscriptions")

    collection = models.ForeignKey(
        "Collection", verbose_name=_("Collection"), on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)
    remind_me = models.BooleanField(_("Remind me"))

    def __str__(self):
        return f"{self.user} -x- {self.collection}"
