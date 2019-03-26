from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button, HTML, Div, Field, Row
from crispy_forms.bootstrap import FormActions, AppendedText, TabHolder, Tab, Accordion, AccordionGroup, PrependedText

from .models import User


__all__ = (
    "UserCreationForm",
    "UserChangeForm",
)


class UserCreationForm(BaseUserCreationForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('username', 'is_admin')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                _("Passwords don't match"),
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User
        fields = '__all__'


class AuthenticationForm(BaseAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Row("username"),
                Row("password")
            )
        )