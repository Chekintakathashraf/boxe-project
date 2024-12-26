from django import forms
from .models import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div,HTML

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
                
                # Name Field
            HTML("""
            <div class="col-span-6 sm:col-span-3">
                <label for="vendor_name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Name</label>
                <input type="text" name="vendor_name" id="vendor_name" value="{{ vendor_form.vendor_name.value|default_if_none:'' }}" class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="Enter your vendor name" required>
                {% if vendor_form.vendor_name.errors %}
                <p class="text-sm text-red-600 dark:text-red-400 mt-1">
                    {{ vendor_form.vendor_name.errors|striptags }}
                </p>
                {% endif %}
            </div>
            """),
            # Email Field
            HTML("""
            <div class="col-span-6 sm:col-span-3">
                <label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Email</label>
                <input type="email" name="email" id="email" value="{{ vendor_form.email.value|default_if_none:'' }}" class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="example@company.com" required>
                {% if vendor_form.email.errors %}
                <p class="text-sm text-red-600 dark:text-red-400 mt-1">
                    {{ vendor_form.email.errors|striptags }}
                </p>
                {% endif %}
            </div>
            """),
            css_class="grid grid-cols-2 gap-4"
            
            
            ),
            Div(
            
            # Address Field
            HTML("""
            <div class="col-span-6 sm:col-span-3">
                <label for="address" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Address</label>
                <input type="text" name="address" id="address" value="{{ vendor_form.address.value|default_if_none:'' }}" class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="ABCD XYZ " required>
                {% if vendor_form.address.errors %}
                <p class="text-sm text-red-600 dark:text-red-400 mt-1">
                    {{ vendor_form.address.errors|striptags }}
                </p>
                {% endif %}
            </div>
            """),
            
            css_class="grid grid-cols-2 gap-4"
        ),
        
            
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
    
    
