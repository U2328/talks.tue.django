from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

__all__ = (
    "UserManager",
    "User",
    "Subscription"
)


class UserManager(BaseUserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_verified', True)
        if extra_fields.get('is_verified') is not True:
            raise ValueError('Superuser must have is_verified=True.')
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    is_verified = models.BooleanField(_("Verified?"), default=False)
    objects = UserManager()

    def is_subscribed_to(self, collection):
        return self.subscriptions.filter(collection=collection).exists()


class Subscription(models.Model):
    class Meta:
        verbose_name = _("subscription")
        verbose_name_plural = _("subscriptions")

    collection = models.ForeignKey('core.Collection', verbose_name=_("Collection"), on_delete=models.CASCADE, related_name="subscriptions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE, related_name="subscriptions")
    remind_me = models.BooleanField(_("Remind me"), default=True)

    FULL_REMINDER = 0
    DAILY_REMINDER = 1
    WEEKLY_REMINDER = 2

    REMINDER_TYPES = (
        (FULL_REMINDER, _("Daily and Weekly")),
        (DAILY_REMINDER, _("Daily")),
        (WEEKLY_REMINDER, _("Weekly")),
    )

    reminder_type = models.PositiveSmallIntegerField(_("Reminder type"), choices=REMINDER_TYPES, default=FULL_REMINDER)

    def __str__(self):
        return f"{self.user} -x- {self.collection}"
