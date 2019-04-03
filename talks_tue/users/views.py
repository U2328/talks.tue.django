from django.contrib import messages
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.views.generic import UpdateView, CreateView, DetailView, DeleteView
from django.http import HttpResponseNotAllowed
from django.utils.http import is_safe_url
from django.utils.translation import gettext as _, gettext_lazy as _l
from django.shortcuts import reverse, redirect, get_object_or_404

from .forms import UserCreationForm, UserChangeForm, SubscriptionChangeForm
from .models import User, Subscription



class SuccessMessageUpdateMixin:
    success_message = None

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class UserMixin(AccessMixin):
    model = User

    def get_object(self, queryset=None):
        return self.request.user

    def get_permission_denied_message(self):
        if self.request.user.is_authenticated:
            return _("Please verfiy your account.")
        return super().get_permission_denied_message()

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_verified):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, _("For greater access please verfiy your account."))
            return redirect("core:index")
        return super().handle_no_permission()


class RegistrationView(CreateView):
    template_name = "users/register.html"
    form_class = UserCreationForm
    success_url = '/'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Check your mail to activate your account."))
        return response


class ProfileView(UserMixin, DetailView):
    template_name = "users/profile.html"


class ProfileUpdateView(UserMixin, SuccessMessageUpdateMixin, UpdateView):
    template_name = "users/update.html"
    form_class = UserChangeForm
    success_message = _l("Check your mail to validate your new email address.")

    def get_success_url(self):
        return reverse("users:profile")


class SubscriptionUpdateView(SuccessMessageUpdateMixin, AccessMixin, UpdateView):
    model = Subscription
    template_name = "users/subscription.html"
    form_class = SubscriptionChangeForm
    success_message = _l("Subscription updated.")

    def dispatch(self, request, pk):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        get_object_or_404(Subscription, pk=pk, user=request.user)
        return super().dispatch(request, pk)

    def get_success_url(self):
        return reverse("users:profile")


@login_required
def subscription_delete(request, pk):
    if request.method == "POST":
        subscription = get_object_or_404(Subscription, pk=pk, user=request.user)
        subscription.delete()
        messages.success(request, _("Subscription removed."))
        redirect_to = request.POST.get('next') or request.GET.get('next')
        return redirect(
            redirect_to
            if redirect is not None and is_safe_url(redirect_to, request.get_host()) else
            "users:profile"
        )
    else:
        raise HttpResponseNotAllowed()
