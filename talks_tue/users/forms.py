from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button, HTML, Div, Field, Row
from crispy_forms.bootstrap import FormActions, AppendedText, TabHolder, Tab, Accordion, AccordionGroup, PrependedText

from .models import User, Subscription


__all__ = (
    "UserCreationForm",
    "UserChangeForm",
    "SubscriptionChangeForm"
)


class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Row(
                    Div(
                        "username",
                        css_class="col"
                    ),
                ),
                Row(
                    Div(
                        "email",
                        css_class="col"
                    ),
                ),
                Row(
                    Div(
                        "password1",
                        css_class="col-sm-6"
                    ),
                    Div(
                        "password2",
                        css_class="col-sm-6"
                    ),
                )
            )
        )


class UserChangeForm(forms.ModelForm):
    username = forms.CharField(label=_('Username'), disabled=True)
    email = forms.EmailField(label=_('Email address'))

    class Meta:
        model = User
        fields = ('username', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Row(
                    Div(
                        "username",
                        css_class="col"
                    ),
                ),
                Row(
                    Div(
                        "email",
                        css_class="col"
                    ),
                ),
            )
        )


class SubscriptionChangeForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ('remind_me', 'reminder_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Div(
                    "remind_me",
                    css_class='col-sm-6'
                ),
                Div(
                    "reminder_type",
                    css_class='col-sm-6'
                ),
            )                
        )