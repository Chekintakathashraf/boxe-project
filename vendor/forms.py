from django import forms
from .models import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div

from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory

from django.utils.translation import gettext_lazy as _

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'email', 'address']  

    def __init__(self, *args, **kwargs):
        super(VendorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Div(Field("vendor_name", css_id="vendor_name", css_class="form-control"),
                    Field("email", css_id="email", css_class="form-control"),
                    css_class="grid grid-cols-2 gap-4"
                ),
                Div(Field("address", css_id="address", css_class="form-control"),
                    css_class="mt-4"
                ),
                css_class="sm:grid grid-cols-1 gap-4"
            )
        )



    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if Vendor.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError(_("This email is already used."), code='unique_email')
        
        return email

    def clean_vendor_name(self):
        vendor_name = self.cleaned_data.get('vendor_name')
        
        
        if Vendor.objects.filter(vendor_name=vendor_name).exclude(id=self.instance.id).exists():
            raise ValidationError(_("This Name is already used."), code='unique_vendor_name')
        
        return vendor_name
    
    
class SequenceForm(forms.ModelForm):
    can_delete = forms.BooleanField(required=False, label='Delete')    
    
    class Meta:
        model = Sequence
        fields = ('type','alpha','numeric','padding',)
        
SequenceFormset = inlineformset_factory(
    Vendor,
    Sequence,
    form=SequenceForm,
    extra=1,
    can_delete=False,
)
    
    
