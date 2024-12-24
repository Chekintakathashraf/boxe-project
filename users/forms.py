from allauth.account.forms import SignupForm, ResetPasswordForm,ChangePasswordForm
from django.contrib.auth import forms as admin_forms
from django.forms import EmailField, CharField
from django.utils.translation import gettext_lazy as _
import re
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from .models import User
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    name = CharField(
        max_length=30,
        required=True,
        help_text="Required.",
        label=_("Name"),
    )

    def save(self, request):
        user = super(UserSignupForm, self).save(request)
        user.name = self.cleaned_data["name"]
        user.save()
        return user


class CustomResetPasswordForm(ResetPasswordForm):
    email = forms.EmailField(max_length=254, required=True, help_text="Required.")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("User with this email does not exist."))
        return email

    def save(self, request, **kwargs):
        self.users = User.objects.filter(email=self.cleaned_data["email"])
        return super().save(request, **kwargs)


    
    
class CustomChangePasswordForm(ChangePasswordForm):
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        
        
        


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number']
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Div(Field("name", css_id="name", css_class="form-control"),
                    Field("email", css_id="email", css_class="form-control"),
                    css_class="grid grid-cols-2 gap-4"
                ),
                Div(Field("phone_number", css_id="phone_number", css_class="form-control"),
                    css_class="mt-4"
                ),
                css_class="sm:grid grid-cols-1 gap-4"
            )
        )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise ValidationError(_("Name must contain at least 3 letters."), code='min_length')
        
        if User.objects.filter(name=name).exclude(id=self.instance.id).exists():
            raise ValidationError(_("This name is already taken."), code='unique_name')
        
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError(_("This email is already used."), code='unique_email')
        
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValidationError(_("Phone number should contain exactly 10 digits."), code='invalid_phone')
        
        if User.objects.filter(phone_number=phone_number).exclude(id=self.instance.id).exists():
            raise ValidationError(_("This phone number is already used."), code='unique_phone')
        
        return phone_number
