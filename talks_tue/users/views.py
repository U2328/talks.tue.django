from django.contrib import messages
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.views.generic import FormView
from django.utils.translation import gettext_lazy as _

from .forms import AuthenticationForm


class LoginView(BaseLoginView):
    template_name = "users/login.html"
    form_class = AuthenticationForm
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Logged in as, %(username)s.") % {"username": self.request.user.username})
        return response


class LogoutView(BaseLogoutView):
    template_name = "users/login.html"
    
    def get(self, request, *args, **kwargs):
        messages.success(request, _("Logged out."))
        return super().get(request, *args, **kwargs)
    