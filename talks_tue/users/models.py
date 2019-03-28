from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


__all__ = (
    "UserManager",
    "User",
)


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username address')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(_('Username'), max_length=32, unique=True)
    is_admin = models.BooleanField(_('Admin?'), default=False)
    email = models.EmailField(_('Email address'), blank=True, null=True, unique=True)
    is_verified = models.BooleanField(_("Verified?"), default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    objects = UserManager()

    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.username


class Subscription(models.Model):
    class Meta:
        verbose_name = _("subscription")
        verbose_name_plural = _("subscriptions")

    limit = models.Q(app_label='core', model='Collection') |\
            models.Q(app_label='core', model='MetaCollection')
    collection_type = models.ForeignKey(ContentType, limit_choices_to=limit, on_delete=models.CASCADE, related_name="subscriptions")
    collection_pk = models.PositiveIntegerField()
    collection = GenericForeignKey('collection_type', 'collection_pk')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)
    remind_me = models.BooleanField(_("Remind me"))

    def __str__(self):
        return f"{self.user} -x- {self.collection}"
