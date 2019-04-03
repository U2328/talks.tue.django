import sys

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
from django_currentuser.db.models import CurrentUserField


__all__ = (
    "HasRevision",
    "create_revision",
    "REVISION_MODEL_MAP"
)

MODEL_MODULE = globals()['__name__'].rsplit('.', 1)[0] + '.models'
REVISION_MODEL_MAP = {}


class RevisionActions:
    CREATE = 0
    CHANGE = 1
    DELETE = 2

    MAP = (
        (CREATE, _("create")),
        (CHANGE, _("change")),
        (DELETE, _("delete")),
    )


def _revision_save(self, *args, **kwargs):
    if not self.original.revisions.exists():
        self.action = RevisionActions.CREATE
    else:
        self.action = RevisionActions.CHANGE
    super(self.__class__, self).save(*args, **kwargs)


def generate_revision_for(model):
    def inner(create_func):
        create_func.__name__ = "create"
        bases = tuple(base for base in model.__bases__ if base.__name__ is not "HasRevision")
        class Meta(*[base.Meta for base in bases if hasattr(base, "Meta")]):
            abstract = False
            ordering = ["-pk"]
            verbose_name = _(f"{model.Meta.verbose_name if hasattr(model.Meta, 'verbose_name') else model.__name__} revision")
            verbose_name_plural = _(f"{model.Meta.verbose_name if hasattr(model.Meta, 'verbose_name') else model.__name__} revisions")

        REVISION_MODEL_MAP[model] = Revision = type(
            f"{model.__name__}Revision", bases,
            {
                "Meta": Meta,
                "__module__": MODEL_MODULE,
                "__str__": lambda revision: f"{revision.original} @ {revision.date_created} [{revision.action}]",
                "save": _revision_save,
                "create": classmethod(create_func),
                "action": models.PositiveSmallIntegerField(verbose_name=_("Revision action"), default=RevisionActions.CHANGE, choices=RevisionActions.MAP),
                "date_created": models.DateTimeField(verbose_name=_("Date created"), default=now),
                "original": models.ForeignKey(verbose_name=_("Original"), to=model._meta.label, on_delete=models.SET_NULL, null=True, blank=True, related_name="revisions"),
                "user": CurrentUserField(verbose_name=_("User"),  on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_actions"),
            }
        )
        return Revision
    return inner


class HasRevision:
    def save(self, *args, no_revision=False, **kwargs):
        super().save(*args, **kwargs)
        if not no_revision:
            create_revision(self)

    def delete(self, *args, **kwargs):
        create_revision(self, delete=True)
        super().delete(*args, **kwargs)


def create_revision(original, *, delete=False):
    revision_class = REVISION_MODEL_MAP.get(original.__class__, None)
    if revision_class is None:
        raise ImproperlyConfigured(f"{original.__class__} is missing a revision counterpart.")
    revision = revision_class.create(original)
    if delete:
        revision.action = RevisionActions.DELETE
        revision.save()
    return revision
