from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .forms import *
from .models import *
from django.db import transaction
from django.core.paginator import Paginator



def create_vendor(request):
    if request.method == 'POST':
        vendor_form = VendorForm(request.POST)
        sequence_formset = SequenceFormset(request.POST, prefix="sequence_formset")
        print("Sequence Formset Data:")
        for form in sequence_formset:
            print(form.data)
        
        if vendor_form.is_valid() and sequence_formset.is_valid():
            with transaction.atomic():
                # Save the vendor only after both forms are valid
                vendor = vendor_form.save()
                
                for form in sequence_formset:
                    if form.cleaned_data:
                        print(form.cleaned_data)
                        if form.cleaned_data.get('type') and form.cleaned_data.get('alpha') and form.cleaned_data.get('numeric') and form.cleaned_data.get('padding'):
                            instance = form.save(commit=False)
                            instance.vendor = vendor
                            
                            if form.cleaned_data.get('can_delete'):
                                instance.delete()
                            else:
                                instance.save()
                        else:
                            print(f"Missing required fields in form {form}")
                
                messages.success(request, 'Vendor created successfully.')  
                return redirect('vendor:vendor_list')
        else:
            # If any formset is not valid, prevent saving the vendor
            if not vendor_form.is_valid():
                print("vendor_form errors:")
                print(vendor_form.errors)
            if not sequence_formset.is_valid():
                print("sequence_formset errors:")
                print(sequence_formset.errors)
            messages.error(request, 'Please correct the errors below.')  
    else:
        vendor_form = VendorForm()  
        sequence_formset = SequenceFormset(prefix="sequence_formset")
        
    return render(request, 'vendor/vendor_form.html', {'vendor_form': vendor_form, 'sequence_formset': sequence_formset, 'title': "Create Vendor"})

def update_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    sequence_qs = Sequence.objects.filter(vendor=vendor)
    
    if request.method == 'POST':
        vendor_form = VendorForm(request.POST, instance=vendor)
        sequence_formset = SequenceFormset(request.POST, prefix="sequence_formset", instance=vendor) 
        
        if vendor_form.is_valid():
            with transaction.atomic():
                vendor_form.save()
                
                if sequence_formset.is_valid():
                    for form in sequence_formset:
                        if form.cleaned_data.get('type') and form.cleaned_data.get('alpha') and form.cleaned_data.get('numeric') and form.cleaned_data.get('padding'):
                            instance = form.save(commit=False)
                            instance.vendor = vendor  
                            if form.cleaned_data.get('can_delete'):
                                instance.delete()
                            else:
                                instance.save()
                    messages.success(request, 'Vendor updated successfully.')
                    return redirect('vendor:vendor_list')
                else:
                    print("Form data:", sequence_formset.data)

                    print('seq-erors',sequence_formset.errors)
                    messages.error(request, 'Please correct the errors in the sequence formset.')
        else:
            print('form-erors',vendor_form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        vendor_form = VendorForm(instance=vendor)
        sequence_formset = SequenceFormset(queryset=sequence_qs, instance=vendor, prefix="sequence_formset")
    
    return render(request, 'vendor/vendor_form.html', {'vendor_form': vendor_form, 'sequence_formset': sequence_formset, 'title': "Update Vendor"})



def vendor_list(request):
    search_query = request.GET.get('search', '')

    vendors = Vendor.objects.all()

    if search_query:
        if not search_query.isdigit():
            vendors = vendors.filter(
                Q(vendor_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        else:
            vendors = vendors.filter(
                Q(phone_number__icontains=search_query)
            )

    paginator = Paginator(vendors, 25)  # 25 entries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vendor/vendor_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'title': "Vendors List",
    })


def vendor_detail(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    return render(request, 'vendor/vendor_detail.html', {'vendor': vendor})


def delete_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    if request.method == 'POST':
        vendor.delete()
        messages.success(request, "Vendor has been deleted successfully.")
        return redirect('vendor:vendor_list')  
    return redirect('vendor:vendor_list')
