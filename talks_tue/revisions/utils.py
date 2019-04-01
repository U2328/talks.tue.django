import sys

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django_currentuser.db.models import CurrentUserField


__all__ = (
    "HasRevision",
    "create_revision",
    "REVISION_MODEL_MAP"
)


REVISION_MODEL_MAP = {}

def generate_revision_for(model):
    def inner(create_func):
        create_func.__name__ = "create"
        bases = tuple(base for base in model.__bases__ if base.__name__ is not "HasRevision")
        class Meta(*[base.Meta for base in bases if hasattr(base, "Meta")]):
            abstract = False
            ordering = ["-pk"]
            verbose_name = _(f"{model.Meta.verbose_name if hasattr(model.Meta, 'verbose_name') else model.__name__} revision")
            verbose_name_plural = _(f"{model.Meta.verbose_name if hasattr(model.Meta, 'verbose_name') else model.__name__} revisions")

        Revision = type(
            f"{model.__name__}Revision", bases,
            {
                "__module__": globals()['__name__'],
                "create": classmethod(create_func),
                "date_create": models.DateTimeField(verbose_name=_("Date created"), default=now),
                "original": models.ForeignKey(verbose_name=_("Original"), to=model._meta.label, on_delete=models.SET_NULL, null=True, blank=True, related_name="revisions"),
                "user": CurrentUserField(verbose_name=_("User"),  on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_actions"),
            }
        )

        REVISION_MODEL_MAP[model] = Revision
        return Revision
    return inner


class HasRevision:
    def save(self, *args, no_revision=False, **kwargs):
        super().save(*args, **kwargs)
        if not no_revision:
            create_revision(self)


def create_revision(original):
    revision_class = REVISION_MODEL_MAP.get(original.__class__, None)
    if revision_class is None:
        raise TypeError(f"No known revision type for objects of type {original.__class__.__name__}")
    return revision_class.create(original)
